import requests
from libraries.utils import generate_token
from daemon_presensesuite.presensesuite_daemon import PresenseSuiteDaemon


URL = 'https://tivit-mobile-orchestrator-ghmgkkc5ea-ue.a.run.app'

# [DEPRECATED]
class PresenceSuiteProcessor():

    def __init__(self):
        pass

    async def call_presencesuite_processor(self, presence_suite: PresenseSuiteDaemon):
        
        payload = {
            'chat_id': presence_suite.chat_id,
            'space_id': presence_suite.space_id,
            'session_presense_suit_id': presence_suite.session_presense_suit_id,
            'token_api_id': presence_suite.token_api_id
        }

        headers = {
            'Authentication': f'Bearer {generate_token(URL)}'
        }

        response = requests.request('POST', url=URL, json=payload, headers=headers)

        print(response)
        return response
    
    async def unlock_status(self, space_id, message):
        url = f'{URL}/api/v1/account/networklockedstatus'
        response = await self.call_tivit_orchestrator(space_id, url, message)

        return response

    async def reset_password(self, space_id, message):
        url = f'{URL}/api/v1/account/networkpassword'
        response = await self.call_tivit_orchestrator(space_id, url, message)

        return response
