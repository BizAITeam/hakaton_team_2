import os
import requests
import json
# from langchain.llms import OpenAI
# os.environ["OPENAI_API_KEY"] = "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"
# llm = OpenAI(temperature=0.9)
# text = "What would be a good company name for a company that makes colorful socks?"
# print(llm(text))

def search(): 
    url = "https://tonai.tech/api/public/v1/services"
    headers={"key":"123456789987654321_f1377930-a14b-4ff1-b394-2c14d2b4d858"}
    response = json.loads(requests.get(url, headers=headers).text)
    #print(response)
    payload ={ 'service_id': "orf9npw80nt7fs4",
            "topic": "How many oceans on the planet",
            "language": "English"
    }
    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    print(response)