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
# aider src/App.jsx src/App.test.js src/About.jsx src/index.jsx --model="azure/gpt-4o --yes"

# Start the backend app.py in a subprocess
backend_process = subprocess.Popen(['python', '/workspace/backend/app.py'])
# Ensure the subprocess is terminated when this script stops executing
atexit.register(backend_process.terminate)

# Set up the model
model = Model("azure/gpt-4o")

# Set up InputOutput with yes=True to automatically confirm prompts
io = InputOutput(yes=True)

# Define the categories with boolean values
# categories_to_include = {
#     'meta': True,
#     'backend_core': True,
#     'backend': True,
#     'backend_test': False,
#     'frontend_core': True,
#     'frontend_content': True,
#     'frontend_test': False
# }
categories_to_include = {
    'meta': True,
    'backend_core': False,
    'backend': False,
    'backend_test': False,
    'frontend_core': True,
    'frontend_content': True,
    'frontend_test': True
}

import os
import json

# Load the JSON file containing the file lists
with open(os.path.join('agent_resources', 'project_files.json'), 'r') as file:
    project_files = json.load(file)

# Example usage
fnames = [file for category, include in categories_to_include.items() if include and category in project_files for file in project_files[category]]
print(fnames)

# Create a coder object
coder = Coder.create(
  main_model=model,
  fnames=fnames,
  io=io,
  use_git=False,
  auto_commits=False,
  auto_test=True,
  # test_cmd="cd /workspace/frontend && npm run test -- --watchAll=false && cd /workspace/backend && pytest tests/test_api.py"
  test_cmd="cd /workspace/frontend && npm run test -- --watchAll=false"
)

# Define the path to the project structure file
project_structure_file_path = os.path.join('agent_resources', 'project_structure.md')

# Read the contents of the project structure file
with open(project_structure_file_path, 'r') as file:
    project_structure = file.read()

guidance = """
Our frontend tests are failing, and we need to determine if the issue is in the frontend code or the test code. We need to fix the issue and ensure that the frontend tests pass successfully.
"""

instructions = """
Determine if the source of the issue is in the frontend code or the test code. Make the necessary changes to resolve the issue and ensure that the frontend tests pass successfully.
"""

# guidance = """
# I want to make sure that everything is setup correctly before further development.
# """

# instructions = """
# Carefully audit the site and make sure that everything is production ready before we proceed with additional feature development.
# """

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
* When adding packages, remember that it is not sufficient to add them to the `package.json` or `requirements.txt` file. You must also install them using `npm install --save` or `pip install`.
* Remember that this is an existing production application that we are updating when you make changes. Before editing, refactoring, or adding a file, you should read the content of the existing file. For example, you should not remove existing functionality, tests, content, or documentation unless explicitly instructed to do so. Your work should be additive unless otherwise specified.

{instructions}
"""

# Run the initial context setup
coder.run(initial_message)

# coder.run("""
# Did you add appropriate unit and integration test coverage on the frontend and backend?

# Do not accidentally remove existing tests by overwriting files. Read the existing tests and make sure that you understand them before adding new ones.

# Evaluate the test changes that you made and add any necessary tests that have not been implemented or updated.

# Running backend tests:
# ```sh
# $ cd /workspace/backend && pytest tests/test_api.py
# ```

# Running frontend tests:
# ```sh
# $ cd /workspace/frontend && npm run test -- --watchAll=false
# ```
# """)

# coder.run("""
# Run tests for the backend and frontend, and fix any issues that you find.

# Running backend tests:
# ```sh
# $ cd /workspace/backend && pytest tests/test_api.py
# ```

# Running frontend tests:
# ```sh
# $ cd /workspace/frontend && npm run test -- --watchAll=false
# ```
# """)


# coder.run(f"""
# I have two metadata files that I use for project maintenance with a mapping of the organization of the files in the webapp:

# * A text representation of the project structure: `/workspace/agent_resources/project_structure.md`
# * An organized JSON representation of the project files in this file: `/workspace/agent_resources/project_files.json`

# Following the work that you just performed, update the metadata files to reflect the changes that you made.
# """)

# coder.run("""
# Read, assess, and update the `/workspace/README.md` file as necessary to reflect the changes that you made.

# Use the contents of the `/workspace/agent_resources/project_structure.md` that you just updated when you write the section of the README.md file under the heading "## Project Structure".
# """)
