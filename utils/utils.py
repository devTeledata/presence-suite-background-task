import requests
import json


class Utils:

    @classmethod
    def get_token(self):
        # url = "https://geru.3corp.com.br/webchat/rest/api/v1/token"

        # < COMENTADO PARA UTILIZA��O NO XCALLY
        #url = "https://webchat.tivit.com/webchat/rest/api/v1/token"
        #headers = {
            # 'authorization': "Basic cHJlc2VuY2VhcGk6cHJlc2VuY2VhcGk=",
            #'authorization': "Basic cHJlc2VuY2VhcGk6cHJlc2VuY2VhcGk=",
            #'cache-control': "no-cache",
            #'postman-token': "6dff3322-923b-7da2-4692-41fdf9a91f4b"
        #    }

        #response = requests.request("GET", url, headers=headers)
        #json_return = json.loads(response.text)
        #return json_return['Data']['Token']
        # > COMENTADO PARA UTILIZA��O NO XCALLY

        # Retorna apikey do usu�rio Xcally
        return "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzc1NDY1NzcsIm5vbmNlIjoiYjVkNDdjNDdlN2M3NDIzZjFmMDgzNWU1YzdiOWQ4ZjIiLCJhdWQiOiI3NThlYzk2My1jY2EzLTljMDMtZDAwMy02NjAxNmEwNjRkOWIiLCJpc3MiOiI3NThlYzk2My1jY2EzLTljMDMtZDAwMy02NjAxNmEwNjRkOWIiLCJzdWIiOiIxIn0.wzLPQhk7AW0gLceuzaSwcCVA81cyQpYlhep6Ug1TUHx2WOckbLGF4uboN-_ZpmLm942U0zXU5TxvZ1NaF6mf8w"

    @classmethod
    def creat_session_presense_suite(self, token_id, payload_session):
        # url = "https://geru.3corp.com.br/webchat/rest/api/v1/sessions"
        # < COMENTADO PARA UTILIZA��O NO XCALLY
        #url = "https://webchat.tivit.com/webchat/rest/api/v1/sessions"

        #payload = {
        #    "ServiceId": payload_session.service_id,
        #    "Name": payload_session.name,
        #    "Email": payload_session.email,
        #    "Language": payload_session.language,
        #    "SessionType": payload_session.session_type,
        #    "RemoteIP": payload_session.remote_ip,
        #}
        #headers = {
        #    "Content-Type": "application/json",
        #    "Authorization": "Bearer {}".format(token_id)
        #}

        #response = requests.request("POST", url, json=payload, headers=headers)
        #location = response.headers.get('location', 'teste/teste').split('/')[-1]
        #return location
        # > COMENTADO PARA UTILIZA��O NO XCALLY

        url = "https://tivit.teledatabrasil.com.br/api/openchannel/accounts/1/notify?apikey={}".format(token_id)

        message = "Iniciou uma sess�o... ServiceId: {}, Name: {}, Email: {}, Language: {}, SessionType: {}, RemoteIP: {}".format(payload_session.service_id, payload_session.name, payload_session.email, payload_session.language, payload_session.session_type, payload_session.remote_ip)

        payload = {
            "from": payload_session.email,
            "body": message,
            "mapKey": "email" # aqui pode mudar, dependendo do que foi setado no Openchannel
        }

        headers = {
            "Content-Type": "application/json"
            #,"Authorization": "Bearer {}".format(token_id)
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response)
        if response.status_code == 200:
            res_json = json.loads(response.text)
            return res_json["interaction"]["id"]
        else:
            return false