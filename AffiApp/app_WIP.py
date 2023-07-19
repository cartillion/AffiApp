# Bring in deps
import os 
from apikey import apikey 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.header('Affi📜⚖️, The Expert Affidavit Writer')
affiant_full_name = st.text_input("Affiant Full Name")
date_of_birth = st.text_input("Date of Birth")
job_title = st.text_input("Job Title")
job_site_name = st.text_input("Job Site Name")
city = st.text_input("City")
state = st.text_input("State")
start_work_year = st.text_input("Start Work Year")
end_work_year = st.text_input("End Work Year")
job_duties_description = st.text_input("Job Duties Description")
product_use_start_year = st.text_input("Product Use Start Year")
product_use_end_year = st.text_input("Product Use End Year")
product_brand_and_name = st.text_input("Product Brand and Name")
product_use_description = st.text_input("Product Use Description")
product_packaging_description = st.text_input("Product Packaging Description")

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write me a youtube video title about {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(script) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
