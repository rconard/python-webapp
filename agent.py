from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import subprocess
import atexit
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Start the backend app.py in a subprocess
backend_process = subprocess.Popen(['python', '/workspaces/python-webapp/backend/app.py'])
# Ensure the subprocess is terminated when this script stops executing
atexit.register(backend_process.terminate)

# Set up the model
model = Model("azure/gpt-4o")

# Set up InputOutput with yes=True to automatically confirm prompts
io = InputOutput(yes=True)

# Define the files to be included in the chat
fnames = [
    "/workspaces/python-webapp/README.md",
    "/workspaces/python-webapp/backend/app.py",
    "/workspaces/python-webapp/backend/requirements.txt",
    "/workspaces/python-webapp/backend/tests/test_api.py",
    "/workspaces/python-webapp/frontend/public/index.html",
    "/workspaces/python-webapp/frontend/src/config.js",
    "/workspaces/python-webapp/frontend/src/App.js",
    "/workspaces/python-webapp/frontend/src/App.test.js",
    "/workspaces/python-webapp/frontend/src/index.js",
    "/workspaces/python-webapp/frontend/package.json"
]

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames, io=io)

# Define the initial context and instructions
initial_message = """
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

The webapp currently only has a very simple home page. We need to add very simple routing to the site with the React Router library (`react-router-dom`).

Important:
* The environment and dependencies are already configured and ready for you to use.
* I have already started the backend app with hot reloading in a subprocess. You can assume that the latest version of the backend API is available at http://localhost:5000.
* Package management for the frontend is done with npm, and for the backend, it is done with pip and a `requirements.txt` file.
* Always update the contents of the `README.md` file when you finish.
* Add unit and integration tests once you finish feature work when appropriate. Do not overwrite existing tests. Read the existing tests and make sure that you understand them before adding new ones.
* Remember that this is an existing production application that we are updating when you make changes. Before editing, refactoring, or adding a file, you should read the content of the existing file. For example, you should not remove existing functionality, tests, content, or documentation unless explicitly instructed to do so. Your work should be additive unless otherwise specified.

Update the site to support routing with the following requirements:
* Add a new page at `/about` that displays a simple message like "This is the about page."
* Add a navigation bar to the top of the site with links to the home page and the about page.
* Add unit tests for the new routing functionality.
"""

# Run the initial context setup
coder.run(initial_message)
