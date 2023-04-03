from schema.PresenceSuite import PresenceSuite
from daemon_presensesuite.presensesuite_daemon import PresenseSuiteDaemon
from model.payload_session import PayloadSession
from utils.utils import Utils


class PresenceSuiteTask:

    def task(self, presensesuite: PresenceSuite):
        #Cria uma sessão de payload
        payload_session = PayloadSession(7777, presensesuite.name, presensesuite.email, "PT", session_type="CHAT",
                                         remote_ip="")

        utils = Utils()

        # Pega o token
        token = utils.get_token()

        #Cria sessão de chat
        chat_session = utils.creat_session_presense_suite(token_id=token, payload_session=payload_session)

        #Cria Daemon
        presensesuite_daemon = PresenseSuiteDaemon(chat_id='Google ChatID', token_api_id=token,
                                                   session_presense_suit_id=chat_session,
                                                   space_id=presensesuite.space_id)
        #Inicia o processamento    
        presensesuite_daemon.process_streming()
