# MVC Template Project

This project is a basic implementation of a Model-View-Controller (MVC) pattern application using Python for the backend and React for the frontend.

## Project Structure

```
python-webapp/
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

## Backend (Python/Flask)

The backend is built using Flask, a lightweight Python web framework. It serves the frontend application and provides an API endpoint for the echo functionality.

Key files:
- `backend/app.py`: Contains the Flask application, route definitions, and API endpoint.
- `backend/requirements.txt`: Lists the Python packages required for the backend.
- `backend/tests/test_api.py`: Contains unit tests for the backend API.

## Frontend (React)

The frontend is a single-page application built with React. It provides a simple user interface to interact with the backend API.

Key files:
- `frontend/public/index.html`: The main HTML file that serves as a template for the React application.
- `frontend/src/App.js`: The main React component that handles the user interface and API interaction, including routing.
- `frontend/src/About.js`: The React component for the About page.
- `frontend/src/index.js`: The entry point for the React application.
- `frontend/package.json`: Defines the Node.js dependencies and scripts for the frontend.

## Development Container

This project includes configuration files for a development container, which provides a consistent development environment across different machines:

- `Dockerfile`: Defines the development environment, including Python, Node.js, and necessary dependencies.
- `.devcontainer/devcontainer.json`: Configures the Visual Studio Code development container, including extensions and settings.

## Getting Started

### Using Visual Studio Code and Dev Containers

1. Install [Visual Studio Code](https://code.visualstudio.com/) and the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
2. Clone this repository and open it in Visual Studio Code.
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command from the Command Palette (F1).
4. VS Code will build the dev container and set up the environment. This may take a few minutes the first time.
5. Once the container is ready, you can run the backend and frontend from the integrated terminal:

   For the backend:
   ```
   python backend/app.py
   ```

   For the frontend:
   ```
   cd frontend && npm start
   ```

6. Open your browser and navigate to `http://localhost:3000` to view the application.

### Manual Setup

If you prefer not to use the dev container, you can set up the project manually:

1. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. Set up the frontend:
   ```
   cd frontend
   npm install
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to view the application.

## Running Tests

### Backend Tests

To run the backend API tests:

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Run the tests using pytest:
   ```
   pytest tests/test_api.py
   ```

   Or, if you prefer to use unittest:
   ```
   python -m unittest tests/test_api.py
   ```

### Frontend Tests

To run the frontend tests:

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Run the tests using Jest:
   ```
   npm test
   ```

This will start Jest in watch mode, which will automatically re-run tests when files are changed.
