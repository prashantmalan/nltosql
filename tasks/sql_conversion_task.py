from crewai import Task

class SQLConversionTask:
    def __init__(self, agent, natural_language_query=None):
        self.agent = agent
        self.query = natural_language_query or "List all users who made a purchase in the last month"
        self.chat_history = []
        self.system_prompt = """You are an expert SQL developer. Your task is to:
        1. Analyze the natural language query
        2. Generate an appropriate SQL query
        3. Explain your reasoning
        4. Consider the database schema provided
        5. Use proper SQL best practices"""

    def add_to_history(self, message, role="user"):
        self.chat_history.append({"role": role, "content": message})

    def get_chat_context(self):
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history[-5:]])  # Keep last 5 messages

    def format_prompt(self):
        return f"""Based on this natural language query: "{self.query}"
        
        Previous conversation context:
        {self.get_chat_context()}
        
        Generate a SQL query that:
        1. Is syntactically correct
        2. Uses the provided schema:
           Database: my_store
           Tables:
           - users (
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(100) NOT NULL,
               email VARCHAR(100) UNIQUE NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           )
           - orders (
               id INT AUTO_INCREMENT PRIMARY KEY,
               user_id INT,
               total_amount DECIMAL(10,2) NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (user_id) REFERENCES users(id)
           )
           
           Sample data characteristics:
           - Around 100 users in the system
           - Up to 10 orders per user
           - Order amounts range from $10 to $1000
           - Order dates span the last 6 months
           
        3. Follows SQL best practices
        4. Includes brief explanation of the approach
        
        Your response should be structured as:
        SQL: <the generated query>
        Explanation: <your brief explanation>"""

    def create(self):
        self.add_to_history(self.query, "user")
        
        return Task(
            description=self.format_prompt(),
            agent=self.agent,
            context=[self.system_prompt],  # Changed to pass as list
            expected_output="A SQL query with explanation"
        )