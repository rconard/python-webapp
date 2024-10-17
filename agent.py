from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import subprocess
import atexit
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Prompt for chat mode
# aider src/App.js src/App.test.js src/About.js src/index.js --model="azure/gpt-4o --yes"

# Start the backend app.py in a subprocess
backend_process = subprocess.Popen(['python', '/workspace/backend/app.py'])
# Ensure the subprocess is terminated when this script stops executing
atexit.register(backend_process.terminate)

# Set up the model
model = Model("azure/gpt-4o")

# Set up InputOutput with yes=True to automatically confirm prompts
io = InputOutput(yes=True)

# Define the files to be included in the chat
fnames = [
    "/workspace/README.md",
    "/workspace/backend/app.py",
    "/workspace/backend/requirements.txt",
    "/workspace/backend/tests/test_api.py",
    "/workspace/frontend/public/index.html",
    "/workspace/frontend/src/config.js",
    "/workspace/frontend/src/App.js",
    "/workspace/frontend/src/App.test.js",
    "/workspace/frontend/src/index.js",
    "/workspace/frontend/package.json"
]

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames, io=io)

# Define the initial context and instructions
initial_message = """
I have a web application that uses a Python backend and a React frontend that we are going to update.

The backend code is in `/workspace/backend`, and the frontend code is in `/workspace/frontend`.

The webapp is organized as follows:

```
/workspace/
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
$ cd /workspace/backend && pytest tests/test_api.py
$ cd /workspace/frontend && npm run test -- --watchAll=false
```

The webapp currently only has a very simple home page. We need to add very simple routing to the site with the React Router library (`react-router-dom`).

Important:
* The environment and dependencies are already configured and ready for you to use.
* I have already started the backend app with hot reloading in a subprocess. You can assume that the latest version of the backend API is available at http://localhost:5000.
* Package management for the frontend is done with pnpm, and for the backend, it is done with pip and a `requirements.txt` file.
* Add unit and integration tests once you finish feature work when appropriate. Do not overwrite existing tests. Read the existing tests and make sure that you understand them before adding new ones.
* Remember that this is an existing production application that we are updating when you make changes. Before editing, refactoring, or adding a file, you should read the content of the existing file. For example, you should not remove existing functionality, tests, content, or documentation unless explicitly instructed to do so. Your work should be additive unless otherwise specified.

Update the site to support routing with the following requirements:
* Add a new page at `/about` that displays a simple message like "This is the about page."
* Add a navigation bar to the top of the site with links to the home page and the about page.
* Add unit tests for the new routing functionality.
"""

# Run the initial context setup
coder.run(initial_message)

coder.run('Did you add appropriate unit and integration test coverage on the frontend and backend? Evaluate the test changes that you made and add any necessary tests that have not been implemented or updated.')

coder.run('Run tests for the backend and frontend, and fix any issues that you find.')

coder.run('Read, assess, and update the /workspace/README.md file as necessary to reflect the changes that you made.')
