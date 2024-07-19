from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase

from sqlalchemy import create_engine


class SqlQueryChain:
    def __init__(self, database_uri,
                 llm=None):
        self.database_uri = database_uri
        self.engine = create_engine(database_uri)

        if not llm:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.llm = llm
        self.database = SQLDatabase(engine=self.engine)

    def run(self, query):
        """
        Executes a SQL query using a LangChain SQL query chain.

        Parameters:
        query (str): The SQL query to be executed.

        Returns:
        dict: A dictionary containing the result of the SQL query. The dictionary will have the following structure:
            {
                "result": [list of query results],
                "error": None (if no error occurred),
                "execution_time": float (execution time in seconds)
            }
        """

        execute_query = QuerySQLDataBaseTool(db=self.database)
        write_query = create_sql_query_chain(self.llm, self.database)
        sql_chain = write_query | execute_query
        return sql_chain.invoke({"question": query})
