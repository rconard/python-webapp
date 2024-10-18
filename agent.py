from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import subprocess
import json
import os
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
with open(os.path.join('agent_resources', 'project_files.json'), 'r') as file:
    fnames = json.load(file)

# Create a coder object
coder = Coder.create(
  main_model=model,
  fnames=fnames,
  io=io,
  use_git=False,
  auto_commits=False,
  auto_test=True,
  test_cmd="cd /workspace/frontend && npm run test -- --watchAll=false && cd /workspace/backend && pytest tests/test_api.py",
)

# Define the path to the project structure file
project_structure_file_path = os.path.join('agent_resources', 'project_structure.md')

# Read the contents of the project structure file
with open(project_structure_file_path, 'r') as file:
    project_structure = file.read()

guidance = """
The webapp currently only has a very simple home page. We need to add very simple routing to the site with the React Router library (`react-router-dom`).
"""

instructions = """
Update the site to support routing with the following requirements:
* Add a new page at `/about` that displays a simple message like "This is the about page."
* Add a navigation bar to the top of the site with links to the home page and the about page.
* Add unit tests for the new routing functionality.
"""

# Define the initial context and instructions
initial_message = f"""
I have a web application that uses a Python backend and a React frontend that we are going to update.

The backend code is in `/workspace/backend`, and the frontend code is in `/workspace/frontend`.

The webapp is organized as follows:

```plaintext
{project_structure}
```

You can run tests to validate both the backend and frontend of the webapp with these 2 steps:
```sh
$ cd /workspace/backend && pytest tests/test_api.py
$ cd /workspace/frontend && npm run test -- --watchAll=false
```

{guidance}

Important:
* The environment and dependencies are already configured and ready for you to use. Do not try to initialize the environment or project. Focus on changes from the existing state that are requested here.
* The backend app is currently running and will always be updated. The latest version of the backend API is available at http://localhost:5000.
* Frontend package managment: `npm` and the `frontend/package.json` file (remember to always use the `--save` flag when adding packages)
* Backend package management: `pip` and the `backend/requirements.txt` file
* Remember that this is an existing production application that we are updating when you make changes. Before editing, refactoring, or adding a file, you should read the content of the existing file. For example, you should not remove existing functionality, tests, content, or documentation unless explicitly instructed to do so. Your work should be additive unless otherwise specified.

{instructions}
"""

# Run the initial context setup
coder.run(initial_message)

coder.run("""
Did you add appropriate unit and integration test coverage on the frontend and backend?

Do not accidentally remove existing tests by overwriting files. Read the existing tests and make sure that you understand them before adding new ones.

Evaluate the test changes that you made and add any necessary tests that have not been implemented or updated.

Running backend tests:
```sh
$ cd /workspace/backend && pytest tests/test_api.py
```

Running frontend tests:
```sh
$ cd /workspace/frontend && npm run test -- --watchAll=false
```
""")

coder.run("""
Run tests for the backend and frontend, and fix any issues that you find.

Running backend tests:
```sh
$ cd /workspace/backend && pytest tests/test_api.py
```

Running frontend tests:
```sh
$ cd /workspace/frontend && npm run test -- --watchAll=false
```
""")


coder.run(f"""
I have two metadata files that I use for project maintenance with a mapping of the organization of the files in the webapp.

# agent_resources/project_structure.md
```plaintext
{project_structure}
```

I also store the list of files that are in the project:

# agent_resources/project_files.json
```json
{fnames}
```

Following the work that you just performed, update the metadata files to reflect the changes that you made.
""")

coder.run("""
Read, assess, and update the /workspace/README.md file as necessary to reflect the changes that you made.

Use the contents of the `agent_resources/project_structure.md` that you just updated when you write the section of the README.md file under the heading "## Project Structure".
""")
