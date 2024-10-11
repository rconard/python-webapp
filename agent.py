from interpreter import interpreter

interpreter.llm.model = "azure/gpt-4o"
interpreter.auto_run = True

interpreter.chat("""
I have a web application that uses a Python backend and a React frontend that we are going to update.

The backend code is in `/workspaces/python-webapp/backend`, and the frontend code is in `/workspaces/python-webapp/frontend`.

The webapp is organized as follows:
```
/workspaces/python-webapp/
│
├── README.md
├── .devcontainer/
│   ├── devcontainer.json # Configuration for VS Code dev container
│   └── Dockerfile          # Dockerfile for creating a dev container
├── backend/
│   ├── app.py          # Main Flask application
│   ├── requirements.txt # Python dependencies
│   └── tests/
│       └── test_api.py # Unit tests for the backend API
│
└── frontend/
    ├── public/
    │   └── index.html  # HTML template
    ├── src/
    │   ├── config.js   # Determine API Base by env
    │   ├── App.js      # Main React component
    │   ├── App.test.js # Tests for the App component
    │   └── index.js    # Entry point for React app
    └── package.json    # Node.js dependencies and scripts
```

You can run tests to validate both the backend and frontend of the webapp with these 2 steps:
```sh
$ cd /workspaces/python-webapp/backend && pytest tests/test_api.py
$ cd /workspaces/python-webapp/frontend && npm run test -- --watchAll=false
```
""")
