from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai.tools import BaseTool
import mysql.connector
import os
from dotenv import load_dotenv
from typing import Any
from pydantic import BaseModel, Field

class QueryInput(BaseModel):
    query: str = Field(description="The natural language query to convert to SQL")

class SQLGeneratorTool(BaseTool):
    name: str = "SQL_Generator"
    description: str = "Generates MySQL-compatible SQL queries from natural language"
    args_schema: type[BaseModel] = QueryInput
    
    def __init__(self, get_schema_func):
        super().__init__()
        self._get_schema_func = get_schema_func

    async def _aexecute(self, query: str, *args: Any, **kwargs: Any) -> str:
        schema = self._get_schema_func()
        return f"""Given the query: {query}
            Generate MySQL-compatible SQL considering these tables and their columns:
            {str(schema)}
            
            Consider these data characteristics:
            - Database contains ~100 users
            - Each user has 0-10 orders
            - Order amounts range $10-$1000
            - Orders span the last 6 months
            
            Return only the SQL query without any explanation."""

    def _execute(self, query: str, *args: Any, **kwargs: Any) -> str:
        schema = self._get_schema_func()
        return f"""Given the query: {query}
            Generate MySQL-compatible SQL considering these tables and their columns:
            {str(schema)}
            
            Consider these data characteristics:
            - Database contains ~100 users
            - Each user has 0-10 orders
            - Order amounts range $10-$1000
            - Orders span the last 6 months
            
            Return only the SQL query without any explanation."""

class SQLExpertAgent:
    def get_mysql_schema(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="my_store"
            )
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            schema = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                schema[table_name] = [col[0] for col in columns]
                
            cursor.close()
            conn.close()
            return schema
        except mysql.connector.Error as err:
            print(f"Error accessing MySQL: {err}")
            return {
                "users": ["id", "name", "email", "created_at"],
                "orders": ["id", "user_id", "total_amount", "created_at"]
            }

    def create(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize ChatGPT with explicit API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        llm = ChatOpenAI(
            api_key=api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.1
        )

        # Create tool instance with schema function
        sql_tool = SQLGeneratorTool(get_schema_func=self.get_mysql_schema)

        return Agent(
            role='SQL Expert',
            goal='Convert natural language queries into accurate MySQL statements',
            backstory="""You are an expert MySQL developer specializing in converting 
            natural language to SQL queries. You understand MySQL-specific syntax and 
            best practices for querying time-series data and managing relationships.""",
            verbose=True,
            allow_delegation=False,
            tools=[sql_tool],
            llm=llm
        )