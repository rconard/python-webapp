from interpreter import interpreter
import subprocess
import atexit

interpreter.llm.model = "azure/gpt-4o"
interpreter.auto_run = True
interpreter.loop = True

# Start the backend app.py in a subprocess
backend_process = subprocess.Popen(['nodemon', '--exec', 'python', '/workspaces/python-webapp/backend/app.py'])

# Ensure the subprocess is terminated when this script stops executing
atexit.register(backend_process.terminate)

messages = interpreter.chat("""
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

Important Context Notes:
* The environment and dependencies are already configured and ready for you to use.
* I have already started the backend app with hot reloading in a subprocess. You can assume that the latest version of the backend API is available at http://localhost:5000.
""")

interpreter.messages = messages
