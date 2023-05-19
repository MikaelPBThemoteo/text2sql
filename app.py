from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import streamlit as st
import pandas as pd
import os   

st.title('Ask to Your Database')

#uploaded_file
uploaded_file = st.file_uploader("Carregue o seu banco de dados:", type='sqlite')

api_key = st.text_input('Digite sua chave da OpenAI API:', '', type='password')
os.environ["OPENAI_API_KEY"] = api_key

#"List the total sales per country. Which country's customers spent the most?"
query = st.text_input('Digite sua pergunta:', '')

if st.button('Submeter'):
    run = (uploaded_file is not None) and (api_key is not None) and (query is not None)
    if run:
        # Lê o conteúdo do arquivo carregado em memória
        content = uploaded_file.read()

        # Grava o arquivo carregado no disco em um local temporário
        with open('temp.sqlite', 'wb') as f:
            f.write(content)

        db = SQLDatabase.from_uri("sqlite:///temp.sqlite")    
        llm = OpenAI(temperature=0)
        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_intermediate_steps=True)
        result = db_chain(query)

        st.write("Resposta:")
        st.write(result['result'])
        st.write("SQLQuery:")
        st.write(result['intermediate_steps'][0])
