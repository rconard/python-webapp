from interpreter import interpreter
import subprocess
import atexit
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

interpreter.llm.model = "azure/gpt-4o"
interpreter.auto_run = True
interpreter.loop = True

# Start the backend app.py in a subprocess
backend_process = subprocess.Popen(['python', '/workspaces/python-webapp/backend/app.py'])

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

<Insert instructions here>

Important:
* The environment and dependencies are already configured and ready for you to use.
* I have already started the backend app with hot reloading in a subprocess. You can assume that the latest version of the backend API is available at http://localhost:5000.
* Package management for the frontend is done with pnpm, and for the backend, it is done with pip and a `requirements.txt` file.
* Always update the contents of the `README.md` file when you finish.
* Add unit and integration tests once you finish feature work when appropriate. Do not overwrite existing tests. Read the existing tests and make sure that you understand them before adding new ones.
* Remember that this is an existing production application that we are updating when you make changes. Before editing, refactoring, or adding a file, you should read the content of the existing file. For example, you should not remove existing functionality, tests, content, or documentation unless explicitly instructed to do so. Your work should be additive unless otherwise specified.
""")

interpreter.messages = messages
