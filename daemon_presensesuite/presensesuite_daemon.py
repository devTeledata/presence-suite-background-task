import requests
import json
import time
from libraries.gcp.sd_chat import ChatClient
from libraries.gcp.sd_firestore import FirestoreClient
from google.cloud import firestore
from datetime import datetime
import jsons

from libraries.gcp.session import SessionManager


class PresenseSuiteDaemon:

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, chat_id, session_presense_suit_id, token_api_id, space_id):
        self.chat_id = chat_id
        self.session_presense_suit_id = session_presense_suit_id
        self.token_api_id = token_api_id
        self.space_id = space_id
        self._db = firestore.Client()
        self.chat_client = ChatClient()
        self.firestore = FirestoreClient()

    def process_streming(self):
        # url = "https://geru.3corp.com.br/webchat/rest/api/v1/sessions/{}/status".format(self.session_presense_suit_id)
        # < COMENTADO PARA UTILIZAÇÃO NO XCALLY
        #url = "https://webchat.tivit.com/webchat/rest/api/v1/sessions/{}/status".format(self.session_presense_suit_id)
        #payload = ""
        #headers = {"Authorization": "Bearer {}".format(self.token_api_id)}
        # > COMENTADO PARA UTILIZAÇÃO NO XCALLY

        # AJUSTE PARA UTILIZAÇÃO NO XCALLY
        #MESSAGES
        #url = "https://tivit.teledatabrasil.com.br/api/openchannel/interactions/{}/messages?apikey={}".format(self.session_presense_suit_id, self.get_token())
        #INTERACAO
        url = "https://tivit.teledatabrasil.com.br/api/openchannel/interactions/{}?apikey={}".format(self.session_presense_suit_id, self.get_token())

        payload = ""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        state = 0

        self.save_session_presence_suite()

        show_history_messages = True

        first_iteration = True

        while True:
            r = requests.request("GET", url, data=payload, headers=headers, stream=True)
            print(r)
            if r.status_code == 200:
                AgentNickName, res_json, state = self.get_variables(r, state)
                print(AgentNickName)

                # O que cada status representa.
                # 2 não tem atendente, 1 atendido, 6 sessão finalizada
                if state == 3 or state == 4 or state == 5 or state == 6 or state == 7 or state == 8 or state == 9:
                    self.set_operator_request_false()
                    break
                else:
                    # print(res_json)
                    # Implementar fazer tratamento de try catch para encerrar o wile com break
                    # toda a lógica de interações de respostas ficam nesse else.
                    if first_iteration:
                        first_iteration = False
                        # Mensagem ao usuário que a sessão foi iniciada e quem é o atendente
                        self.chat_client.send_message_to_user(text="Você está sendo atendido por {}"
                                                              .format(AgentNickName),
                                                              space_name='spaces/{}'.format(self.space_id))

                    if state == 1 and show_history_messages:
                        show_history_messages = False
                        query = self.firestore._db.collection(
                            f'spaces/{self.space_id}/sessions').order_by(
                            u'_id', direction=self.firestore.firestore_lib.Query.DESCENDING).limit(1)

                        docs = query.stream()

                        for doc in docs:
                            messages = doc.to_dict()['messages']
                            # Mensagem ao atendente com o histórico de mensagens do usuário com o Bot
                            text_formatted = "Segue o histórico de conversa do Cliente com o ChatBot:  "
                            for mess in messages:
                                text_formatted += mess['from']
                                text_formatted += " : "
                                text_formatted += mess['message']
                                text_formatted += "  "
                            self.send_message_chat_to_operator(text_formatted, self.session_presense_suit_id)

                    if res_json["Data"] is not None:
                        if len(res_json["Data"]["Text"]) > 0:
                            self.chat_client.send_message_to_user(text=res_json["Data"]["Text"][0],
                                                                  space_name='spaces/{}'.format(self.space_id))

                    time.sleep(1)
            elif r.status_code != 200:
                # Mensagem de erro caso sessão não seja encontrada
                #   ou ocorra algum erro durante a chamada da sessão
                self.set_operator_request_false(message="Ops. Sua sessão com o operador foi encerrada.")
                break

    def get_variables(self, r, state):
        res_json = json.loads(r.text)
        # > COMENTADO PARA UTILIZAÇÃO NO XCALLY
        #state = res_json["Data"]["State"]
        #AgentNickName = res_json["Data"]["AgentNickName"]
        # > COMENTADO PARA UTILIZAÇÃO NO XCALLY

        #Se estiver encerrada
        if res_json["closed"]:
            state = 6
        #Se não tiver atendente
        elif res_json["UserId"] is None:
            state = 2
        #Se tiver atendente
        else:
            state = 1

        AgentNickName = res_json["UserId"]
        return AgentNickName, res_json, state

    # Mensagem caso o atendente encerre a sessão
    def set_operator_request_false(self, message="Sessão com atendente foi encerrada!"):
        space_info = self._db.collection(f'spaces').document(self.space_id)
        space_info = space_info.get().to_dict()
        session_manager = SessionManager()
        session_manager.end_session(self.space_id)

        if space_info is not None:
            space_info['operator_request'] = False
            space_info['last_interaction'] = datetime.now()
            space_info['session_presense_suit_id'] = None
            self._db.collection(f'spaces').document(self.space_id).set(space_info)
            self.chat_client.send_message_to_user(text=message,
                                                  space_name='spaces/{}'.format(self.space_id))

            query = self.firestore._db.collection(
                f'spaces/{self.space_id}/sessions').order_by(
                u'_id', direction=self.firestore.firestore_lib.Query.DESCENDING).limit(1)

            docs = query.stream()

            for doc in docs:
                id = doc.to_dict()['_id']
                self._db.document(f'spaces/{self.space_id}/sessions/{id}').update(
                    {'operator_request': False})

    def save_session_presence_suite(self):
        print(self.space_id)
        space_info = self._db.collection(f'spaces').document(self.space_id)
        space_obj = space_info.get()
        if space_obj is not None:
            doc = space_obj.to_dict()
            doc['last_interaction'] = datetime.now()
            doc['session_presense_suit_id'] = self.session_presense_suit_id
            self._db.collection(f'spaces').document(self.space_id).set(doc)

    def send_message_chat_to_operator(self, message, session):

        # url = "https://geru.3corp.com.br/webchat/rest/api/v1/sessions/{}/text".format(session)
        # url = "https://webchat.tivit.com/webchat/rest/api/v1/sessions/{}/text".format(session)
        url = "https://tivit.teledatabrasil.com.br/api/openchannel/accounts/1/notify?apikey=".format(self.get_token())
        url_teste = "http://sssaude.teledatabrasil.com.br:3333/post-teste-recebe.php"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "Authorization": "Bearer {}".format(self.get_token())
        }

        # Formato de dados recebido pelo Xcally
        params = {
            "from": session,
            "body": message,
            "mapKey": "email" # aqui pode mudar, dependendo do que foi setado no Openchannel
        }

        #response = requests.request("POST", url, json=message, headers=headers)
        response = requests.request("POST", url, json=params, headers=headers)
        print(response)
        print(response.text)

        response = requests.request("POST", url_teste, json=params, headers=headers)
        print(response)
        print(response.text)

    def get_token(self):
        # url = "https://geru.3corp.com.br/webchat/rest/api/v1/token"

        # < COMENTADO PARA UTILIZAÇÃO NO XCALLY
        #url = "https://webchat.tivit.com/webchat/rest/api/v1/token"
        #headers = {
            #'authorization': "Basic cHJlc2VuY2VhcGk6cHJlc2VuY2VhcGk=",
            #'cache-control': "no-cache",
            #'postman-token': "6dff3322-923b-7da2-4692-41fdf9a91f4b"
        #}

        #response = requests.request("GET", url, headers=headers)
        #json_return = jsons.loads(response.text)
        #return json_return['Data']['Token']
        # > COMENTADO PARA UTILIZAÇÃO NO XCALLY

        # Retorna apikey do usuário Xcally
        return "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzc1NDY1NzcsIm5vbmNlIjoiYjVkNDdjNDdlN2M3NDIzZjFmMDgzNWU1YzdiOWQ4ZjIiLCJhdWQiOiI3NThlYzk2My1jY2EzLTljMDMtZDAwMy02NjAxNmEwNjRkOWIiLCJpc3MiOiI3NThlYzk2My1jY2EzLTljMDMtZDAwMy02NjAxNmEwNjRkOWIiLCJzdWIiOiIxIn0.wzLPQhk7AW0gLceuzaSwcCVA81cyQpYlhep6Ug1TUHx2WOckbLGF4uboN-_ZpmLm942U0zXU5TxvZ1NaF6mf8w"
