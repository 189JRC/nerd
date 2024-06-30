### Named Entity Recognition Diagramiser

#### Purpose: A tool to analyse text documents with Natural Language Processing

Flask backend, vue/nginx frontend and postgres db.

#### Run Locally

Start flask development server:
- python3 -m venv venv
- source venv/bin/activate
- cd /backend
- pip install -r requirements.txt
- python3 app.py

Start Vite front end development server:
- ensure Node >= 18 is installed
- cd /frontend
- npm install -i
- npm run build
- npm run dev

frontend accessible on http://0.0.0.0:5173

#### Notes

This application was built out of my web scaffolding framework with my preferred configuration.
The files that are most relevant to the NERD application are:

backend/app.py
backend/Investigation.py

frontend/js/Investigation.js
frontend/components/EntryPoint.vue
