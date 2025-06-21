
 Natural Language to SQL Converter

 Overview
This project is an AI-powered tool that converts natural language queries into MySQL-compatible SQL statements. It leverages CrewAI's agent-based architecture and OpenAI's GPT models to simplify database interactions, making SQL knowledge optional for users.

 Features
- Natural Language Input: Query databases using plain English.
- Schema Awareness: Automatically adapts to the database structure.
- Context Maintenance: Tracks conversation history for better query generation.
- Error Handling: Provides clear feedback for invalid queries.
- SQL Best Practices: Generates optimized SQL queries.

 Project Structure
```
demo.db                 SQLite database for testing
init_db.py              Script to initialize the SQLite database
main.py                 Entry point for the interactive CLI application
mysql_init.py           Script to initialize the MySQL database
query                   Placeholder for database query testing
requirements.txt        Python dependencies
agents/
    sql_agent.py        SQL Expert Agent implementation
tasks/
    sql_conversion_task.py  SQL Conversion Task implementation
```

 Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nltosql
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a .env file in the project root.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=<your-api-key>
     ```

 Usage
 Initialize the Database
- For SQLite:
  ```bash
  python init_db.py
  ```
- For MySQL:
  ```bash
  python mysql_init.py
  ```

 Run the Application
Start the interactive CLI application:
```bash
python main.py
```

 Example Query
Input:
```
"Show me all users who spent more than $500 in total"
```

Output:
```sql
SELECT u.name, SUM(o.total_amount) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING total_spent > 500;
```

 Key Components
 SQL Expert Agent (`agents/sql_agent.py`)
- Implements a specialized agent with deep knowledge of SQL.
- Uses OpenAI's GPT-3.5 for natural language understanding.
- Includes a custom SQLGeneratorTool for query generation.

 SQL Conversion Task (`tasks/sql_conversion_task.py`)
- Manages the query conversion pipeline.
- Provides structured prompts to ensure SQL best practices.
- Maintains conversation history for context-aware query generation.

 Interactive CLI Application (`main.py`)
- Offers a user-friendly interface for query input.
- Handles errors gracefully and provides real-time feedback.

 Future Enhancements
- Support for more complex schemas and databases.
- Web-based interface for broader accessibility.
- Query optimization suggestions.
- Multi-language support for global users.

 License
This project is licensed under the MIT License.

---

Let me know if you'd like to add or modify any section! Key Components
 SQL Expert Agent (`agents/sql_agent.py`)
- Implements a specialized agent with deep knowledge of SQL.
- Uses OpenAI's GPT-3.5 for natural language understanding.
- Includes a custom SQLGeneratorTool for query generation.

 SQL Conversion Task (`tasks/sql_conversion_task.py`)
- Manages the query conversion pipeline.
- Provides structured prompts to ensure SQL best practices.
- Maintains conversation history for context-aware query generation.

 Interactive CLI Application (`main.py`)
- Offers a user-friendly interface for query input.
- Handles errors gracefully and provides real-time feedback.

 Future Enhancements
- Support for more complex schemas and databases.
- Web-based interface for broader accessibility.
- Query optimization suggestions.
- Multi-language support for global users.

 License
This project is licensed under the MIT License.
