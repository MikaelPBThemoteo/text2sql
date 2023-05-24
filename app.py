from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import streamlit as st
import pandas as pd
import os   
from langchain.agents import create_csv_agent

with st.sidebar:
    st.header('Sobre')
    st.markdown('Obrigado pelo seu interesse na nossa aplicação. Por favor, \
                esteja ciente de que este é apenas um sistema de Prova de \
                Conceito e pode conter bugs ou recursos inacabados.')
    st.markdown('Feito por [Hagi Jakobson](https://www.linkedin.com/in/hagijakobson/) e [Mikael Timoteo](https://www.linkedin.com/in/mikael-themoteo-00869574/).')
    st.markdown('O código fonte pode ser encontrado [aqui](https://github.com/MikaelPBThemoteo/text2sql).')
    
st.title('Pergunte A Sua Base de Dados')

option = st.selectbox('Qual o tipo da sua base de dados?',
                      ('SQLITE', 'CSV'))
#uploaded_file
uploaded_file = st.file_uploader("Carregue a sua base de dados:", 
                                type=option.lower())

# Authentication
api_key = st.text_input('Digite sua chave da OpenAI API:', '', type='password')
os.environ["OPENAI_API_KEY"] = api_key

#"List the total sales per country. Which country's customers spent the most?"
query = st.text_input('Digite sua pergunta:', '')

if st.button('Submeter'):
    run = ((uploaded_file is not None) and (api_key is not None) and 
           (query is not None))
    if run:
        if option == 'SQLITE':
            # Lê o conteúdo do arquivo carregado em memória
            content = uploaded_file.read()

            # Grava o arquivo carregado no disco em um local temporário
            with open('temp.sqlite', 'wb') as f:
                f.write(content)

            db = SQLDatabase.from_uri("sqlite:///temp.sqlite")    
            llm = OpenAI(temperature=0)
            db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, 
                                        return_intermediate_steps=True)
            result = db_chain(query)

            st.write("Resposta:")
            st.write(result['result'])
            st.write("SQLQuery:")
            st.write(result['intermediate_steps'][0])
        else:
            # Lê o conteúdo do arquivo carregado em memória
            content = uploaded_file.read()
            
            # Grava o arquivo carregado no disco em um local temporário
            with open('temp.csv', 'wb') as f:
                f.write(content)
            
            agent = create_csv_agent(OpenAI(temperature=0), 
                                    'temp.csv', verbose=True)
            
            result = agent.run(query)
            st.write("Resposta:")
            st.write(result)
