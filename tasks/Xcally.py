from schema.Xcally import Xcally
from daemon_presensesuite.xcally_daemon import XcallyDaemon
from model.payload_session import PayloadSession
from utils.utils import Utils


class XcallyTask:

    def task(self, xcally: Xcally):
        utils = Utils()

        # Pega o token
        token = utils.get_token()

        #Cria Daemon
        xcally_daemon = XcallyDaemon(token_api_id=token, session_xcally=xcally)
        #Inicia o processamento    
        xcally_daemon.process_streming()
