from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from dotenv import load_dotenv

# Load enviroment variables
load_dotenv()

db = SQLDatabase.from_uri("sqlite:///Chinook.sqlite")
llm = OpenAI(temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_intermediate_steps=True)
result = db_chain("List the total sales per country. Which country's customers spent the most?")
