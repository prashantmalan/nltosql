import os
from dotenv import load_dotenv
from crewai import Crew
from agents.sql_agent import SQLExpertAgent
from tasks.sql_conversion_task import SQLConversionTask

# Load environment variables
load_dotenv()

class SQLConversation:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.sql_expert = SQLExpertAgent().create()
        self.task = SQLConversionTask(agent=self.sql_expert)
        self.crew = Crew(
            agents=[self.sql_expert],
            tasks=[],
            verbose=True
        )

    def process_query(self, natural_language_query):
        try:
            self.task.query = natural_language_query
            sql_task = self.task.create()
            self.crew.tasks = [sql_task]
            result = self.crew.kickoff()
            self.task.add_to_history(result, "assistant")
            return result
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            self.task.add_to_history(error_msg, "system")
            return error_msg

def interactive_sql_session():
    try:
        conversation = SQLConversation()
        print("Welcome to the SQL Query Generator!")
        print("Using OpenAI GPT-3.5 for query generation")
        print("Type 'exit' to end the conversation.")
        
        while True:
            query = input("\nEnter your query: ").strip()
            if query.lower() == 'exit':
                break
                
            result = conversation.process_query(query)
            print("\nGenerated Response:")
            print(result)
            
    except Exception as e:
        print(f"Session Error: {str(e)}")
        print("Please make sure OPENAI_API_KEY is set in your environment variables")

if __name__ == "__main__":
    interactive_sql_session()