import requests
import json
import time
from libraries.gcp.sd_chat import ChatClient
from libraries.gcp.sd_firestore import FirestoreClient
from google.cloud import firestore
from datetime import datetime
import jsons

from libraries.gcp.session import SessionManager


class XcallyDaemon:

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, token_api_id, session_xcally):
        self.token_api_id = token_api_id
        self.session_xcally = session_xcally
        self._db = firestore.Client()
        self.chat_client = ChatClient()
        self.firestore = FirestoreClient()

    def process_streming(self):
        self.space_id = self.session_xcally.OpenchannelInteractionId

        self.save_session_presence_suite()

        if self.session_xcally.body is not None:
            if len(self.session_xcally.body) > 0:
                self.chat_client.send_message_to_user(text=self.session_xcally.body,
                                                        space_name='spaces/{}'.format(self.space_id))
        else:
            # Mensagem de erro caso sessão não seja encontrada
            #   ou ocorra algum erro durante a chamada da sessão
            self.set_operator_request_false(message="Ops. Erro ao receber a mensagem.")

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