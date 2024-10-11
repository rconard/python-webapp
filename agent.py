from interpreter import interpreter

interpreter.llm.model = "azure/gpt-4o"
interpreter.auto_run = True

interpreter.chat("""
I have a web application that uses a Python backend and a React frontend that we are going to update.

The backend code is in `/workspaces/python-webapp/backend`, and the frontend code is in `/workspaces/python-webapp/frontend`.

You can run the webapp with these 2 steps:
```sh
$ cd /workspaces/python-webapp/frontend && npm run build
$ cd /workspaces/python-webapp/backend && python app.py
```

These steps build the frontend React application and start the Flask server.
                 
You can run the unit tests for the backend API with this command:
```sh
$ cd /workspaces/python-webapp/backend && pytest tests/test_api.py
```
""")
