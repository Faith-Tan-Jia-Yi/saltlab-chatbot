import dialogflow_v2beta1 as dialogflow
import json
from google.protobuf.json_format import MessageToJson

project_id = "coachingbot-mvhd"
credentials_path = "creds.json"

class SessionClient:

    def __init__(self,credentials_path=credentials_path, project_id=project_id):
        self.project_id = project_id
        self.session_client = dialogflow.SessionsClient.from_service_account_json(credentials_path)
        self.session_ = self.session_client.session_path(self.project_id,'1001')
        self.sessions = {}
        self.lastsession = 100000
    
    def createSession(self):
        self.lastsession += 1
        session = self.session_client.session_path(self.project_id,str(self.lastsession))
        self.sessions[self.lastsession] = session
        return self.lastsession
    
    def detectIntent(self,text):
        text_input = dialogflow.types.TextInput(text=text, language_code='en')
        query_input = dialogflow.types.QueryInput(text=text_input)
        return self.session_client.detect_intent(session=self.session_, query_input=query_input)

    def dialogflow(self, question):
        resp = self.detectIntent(question)
        json_response = MessageToJson(resp)
        r = json.loads(json_response)

        response_id = r['responseId']
        query_result = r['queryResult']
        query_text = query_result['queryText']
        intent = query_result['intent']
        action = query_result['action']
        parameters = query_result['parameters']

        print(r)
        print("...")
        print(response_id)
        print(query_result)
        print(query_text)
        print(intent)
        print(action)
        print(parameters)

sess = SessionClient()
sess.dialogflow("Hello")
