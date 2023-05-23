import os
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from tonai import TonAI
from langchain.prompts import PromptTemplate


PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
llm = TonAI(temperature=0.7)
summary_chain = load_summarize_chain(llm, chain_type="refine", question_prompt=PROMPT)