from google.cloud import dialogflow

import google.auth

CREDENTIALS, PROJECT_ID = google.auth.default()

class DialogflowClient():

    def __init__(self, session_id):
        self.session_id = session_id
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(PROJECT_ID, session_id)
    
    def detect_intent(self, message):
        print(f'Session id:', self.session_id)

        text_input = dialogflow.TextInput(text=message, language_code="pt-BR")
        query_input = dialogflow.QueryInput(text=text_input)

        df_response = self.session_client.detect_intent(
            request={"session": self.session, "query_input": query_input})

        print("="*50)
        print(f"Query text: {df_response.query_result.query_text}")
        print(f"Detected intent: {df_response.query_result.intent.display_name}")
        print(f"(confidence: {df_response.query_result.intent_detection_confidence})")
        print(f"(output context: {df_response.query_result.output_contexts})")
        print(f"Fulfillment text: {df_response.query_result.fulfillment_text}\n")
    
        # message = f'DF response, {df_response.query_result.fulfillment_text}'

        return df_response.query_result
