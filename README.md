# book_genai

## Steps for setup and execution of the application.

1. Clone git repository
2. Create a virtual environment
3. Change directory to project directory
4. Activate a virtual environment
5. Install requirement.txt using pip to install require dependencies
6. Before starting the application make sure you have an installed Ollama setup using this link: https://ollama.com/download/windows
7. Once you make sure Ollama setup is completed run your application using this command in terminal: "fastapi run main.py"
8. To run test cases run this command in terminal: "pytest"

Note: All the above mentioned steps are for the Windows operating system.


## Open Swagger UI and check endpoints
1. "/docs" using this endpoint access the Swagger UI documentation.
2. use token endpoint to generate bearer token to authenticate the endpoint using authorization option available on swagger ui
3. to generate bearer token use these creds: "username": "testuser", "password": "secretpassword"
