import os
from dotenv import load_dotenv
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI

import requests
import urllib3
from bs4 import BeautifulSoup
import json

import Use_out

load_dotenv()

prompt_template_1 = """Ти виконуєш роль юридичного радника. Проаналізуй запит користувача, написаний простою "людською" мовою та підбери короткі ключові слова, за якими краще шукати відповіді у спеціальній базі знань судових рішень, подай їх як строку, де ключові слова розділяються "AND".
Відповідь має мати 2-3 слова 
Відповідь має бути лише строка для пошуку.

Питання:
"{msg_text}"
"""
prompt_template_2 = """Контекст:
"{context}"

Питання користувача:
"{msg_text}"

Action:
Ти виконуєш роль юридичного радника. Сформулюй коротку відповідь на питання користувача зрозумілою йому мовою. Якщо попередня відповідь "ні" - запропонуй варіанти чи поясни в якому випадку відповідь буде "так".
"""

openai_api_key = os.getenv("OPENAI_API_KEY")
last_query = []

def get_last_query_data():
    with open("db.json", "r") as f:
        data = json.load(f)
    return data


def recognize_key_words(msg_text):
    llm = OpenAI(temperature=0)
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template_1)
    )

    res = llm_chain.run(msg_text)
    return res


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_conclusion_info(finder):
    list_answer = []
    url = f'https://courtpractice.searcher.api.zakononline.com.ua/v1/search?limit=3&search={finder}&target=text'

    # print('ahhhahahahahahah',url)
    headers = {
        'X-App-Token': 'BAD16Q-RZ0ZRG-LA$FAP-BQLOPE-AS361O-%^ASD1-VMD2AS-HS2(2!',
        # 'X-User-Token': 'BAD16Q-RZ0ZRG-LA$FAP-BQLOPE-AS361O-%^ASD1-VMD2AS-HS2(2!',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.get(url, headers=headers, verify=False)
    for i in response.json():
        id_info = i['id']

        url_2 = f'https://courtpractice.searcher.api.zakononline.com.ua/v1/document/by/id/{id_info}'#provider/sphinx'
        response_2 = requests.get(url_2, headers=headers, verify=False)
        text_info = response_2.json()[0]['text']
        start, end = text_info.lower().find('висновки'), text_info.lower().find('ключові слова')
        result = text_info[start + len("висновки"):end]
        soup = BeautifulSoup(result, 'html.parser')
        clear_text = soup.get_text()
        answer = {'id':id_info, 'text':clear_text, 'url':i['url']}
        list_answer.append(answer)

    return list_answer


def create_context(last_query):
    context = ""
    for obj in last_query:
        context = context + '\n' + obj["text"]
    return context


def get_conclusion(form_context, msg_text):
    prompt = PromptTemplate(template=prompt_template_2, input_variables=["context", "msg_text"])
    max_tokens = 4097 - len(form_context) - len(msg_text)
    llm_chain = LLMChain(prompt=prompt, llm=ChatOpenAI(temperature=0, max_tokens=None))

    res = llm_chain.predict(context=form_context, msg_text=msg_text)
    return res


def format_response(txt):
    response = txt + "\n\n" + "https://zakononline.com.ua/"
    return response


def zakon_helper_main(id, msg_text):
    key_words = recognize_key_words(msg_text)
    last_query = get_conclusion_info(key_words)
    with open("db.json", "w") as f:
        json.dump(last_query, f)
    form_context = create_context(last_query)
    conclusion = get_conclusion(form_context, msg_text)
    res = format_response(conclusion)

    print(last_query)
    Use_out.use_out(id, res)


if __name__ == "__main__":
    zakon_helper_main("""В мене помер рідний брат. 
    Проте я пропустив термін прийняття спадщини через те, що сам проходив стаціонарне лікування в клініці 
    від раку, про що маю підтверджуючі документи. Я хочу знайти правову позицію яка дозволить мені прийняти
    спадщину""")
