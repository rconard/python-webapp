/workspace/
│
├── README.md
├── .devcontainer/
│   ├── devcontainer.json # Configuration for VS Code dev container
│   └── Dockerfile        # Dockerfile for creating a dev container
├── backend/
│   ├── app.py            # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   └── tests/
│       └── test_api.py   # Unit tests for the backend API
│
└── frontend/
    ├── public/
    │   └── index.html    # HTML template
    ├── src/
    │   ├── About.jsx     # About page component
    │   ├── config.js     # Determine API Base by environment
    │   ├── App.jsx       # Main React component with routing
    │   ├── App.test.js   # Tests for the App component
    │   ├── index.jsx     # Entry point for React app
    │   ├── Home.jsx      # Home component
    └── package.json      # Node.js dependencies and scripts
