import json

from langchain.tools.base import BaseTool
import requests

class TonAI(BaseTool):
    name = "Summarization"
    description = """Summarizes provided content"""

    headers={"key":"key_tonai_3f26efbb-3f4f-41ab-8abc-824460a947f8"}
    payload ={
    'service_id': "6j99xutxsmiwpt6",
    'temperature' : 0.7
    }
    '''For Gmail'''
    def _run(self, text:str) -> str:
        messages  = [{"role":"user", "content":"""Your job is to write a brief, concise summary, at most 100 symbols, of the following email message.
        `The email's subject appears in the first line.
        Provide an email priority as a rank from 1 to 5, where 1 is an important, urgent message required immediate response, and 5 is a spam. 
        Generate a brief response to the given email. 
        Return a result in the format:

        SUMMARY=summary
        PRIORITY=priority
        RESPONSE=response

        "{text}"
        CONCISE SUMMARY:""".replace("{text}", text)}]
        self.payload["messages"] = json.dumps(messages, ensure_ascii=False)

        response = json.loads(requests.post(url = "https://tonai.tech/api/public/v1/services", json = self.payload, headers=self.headers).text)

        try:
            gpt_response  = json.loads(response.get("messages")[0]["text"])
            assistant_answer = gpt_response["choices"][0]["message"]["content"]

        except Exception as e:
            error = str(e)
            return error
        
        return assistant_answer
    

    

    def _arun(self, text: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Instagram post generation does not support async currently.")
    


