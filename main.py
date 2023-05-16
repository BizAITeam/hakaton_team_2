import os
import json
from dotenv import load_dotenv

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI

import requests
import urllib3
from bs4 import BeautifulSoup

from Use_out import use_out

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE_1 = """Ти виконуєш роль юридичного радника. Проаналізуй запит користувача, написаний простою 
"людською" мовою та підбери короткі ключові слова, за якими краще шукати відповіді у спеціальній базі знань судових
 рішень, подай їх як строку, де ключові слова розділяються "AND".
Відповідь має мати 2-3 слова 
Відповідь має бути лише строка для пошуку.

Питання:
"{msg_text}"
"""

PROMPT_TEMPLATE_2 = """Контекст:
"{context}"

Питання користувача:
"{msg_text}"

Action:
Ти виконуєш роль юридичного радника. Сформулюй коротку відповідь на питання користувача зрозумілою йому мовою. Якщо 
попередня відповідь "ні" - запропонуй варіанти чи поясни в якому випадку відповідь буде "так".
"""

last_query = []


def get_last_query_data():
    with open("db.json", "r") as file:
        data = json.load(file)
    return data


def recognize_key_words(msg_text: str) -> str:
    """
    Analyzes the text of the user's request and selects short keywords for searching in the knowledge base of court
    decisions.

    Arguments:
    - msg_text (str): User request text.

    Returns:
    - str: Keywords to search as a string, separated by the "AND" operator.
    """
    llm = OpenAI(temperature=0)
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(PROMPT_TEMPLATE_1)
    )

    return llm_chain.run(msg_text)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_conclusion_info(finder: str) -> list:
    """
    Gets the conclusion information from the API based on the given search query.

    Arguments:
    - finder (str): Query to find conclusions.

    Returns:
    - list: List of dictionaries with information about conclusions. Each dictionary contains the
    keys 'id' (conclusion identifier), 'text' (conclusion text) and 'url' (source URL).
    """

    list_answer = []
    # URL with limit for three documents
    # url = f'https://courtpractice.searcher.api.zakononline.com.ua/v1/search?limit=3&search={finder}&target=text'

    # URL with limit for only one document
    url = f'https://courtpractice.searcher.api.zakononline.com.ua/v1/search?limit=1&search={finder}&target=text'

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


def create_context(last_query: list) -> str:
    """
    Creates a context string based on the last_query.

    Arguments:
    - last_query (list): List of dictionaries containing the last query information. Each dictionary should
    have the key 'text' representing the text of the query.

    Returns:
    - str: A string representing the context created by joining the text from each query in the 'last_query'
    list with newline characters.
    """
    result = '\n'.join([i["text"] for i in last_query])
    return result


def get_conclusion(form_context, msg_text):
    """
    Generates a conclusion using the form context and message text.

    Arguments:
    - form_context (str): The context of the form, typically a string or structured data representing the context.
    - msg_text (str): The message text or input for generating the conclusion.

    Returns:
    - str: The generated conclusion as a result of processing the form context and message text.
    """
    prompt = PromptTemplate(template=PROMPT_TEMPLATE_2, input_variables=["context", "msg_text"])
    # max_tokens = 4097 - len(form_context) - len(msg_text)
    llm_chain = LLMChain(prompt=prompt, llm=ChatOpenAI(temperature=0, max_tokens=None))

    result = llm_chain.predict(context=form_context, msg_text=msg_text)
    return result


def format_response(txt):
    result = txt + "\n\n" + "https://zakononline.com.ua/"
    return result


def zakon_helper_main(id_of_chat, msg_text):
    # Search for keywords in a message
    key_words = recognize_key_words(msg_text)

    # Getting data from API by keywords
    last_query = get_conclusion_info(key_words)
    # Writing data to a temporary db
    with open("db.json", "w") as file:
        json.dump(last_query, file)

    # Combine the found API data(dict field 'text') into a string
    form_context = create_context(last_query)

    # Forming a conclusion with the help of AI
    # TODO: Turn on for correct work
    # conclusion = get_conclusion(form_context, msg_text)
    # TODO: Delete for correct work
    conclusion = form_context[2:].capitalize()

    # Forming a result
    result = format_response(conclusion)

    # print(result)

    # Calling the messenger function
    use_out(id_of_chat, result)


if __name__ == "__main__":
    zakon_helper_main(1, """В мене помер рідний брат. 
    Проте я пропустив термін прийняття спадщини через те, що сам проходив стаціонарне лікування в клініці 
    від раку, про що маю підтверджуючі документи. Я хочу знайти правову позицію яка дозволить мені прийняти
    спадщину""")
