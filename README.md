### Scaffolding for Web Application

#### Purpose: A Containerised full web application. Starting point for any future website building. 

Flask backend, vue/nginx frontend and postgres db.

#### Local Development.

Start flask development server:
- cd /backend
- python3 app.py

Start Vite front end development server:
- cd /frontend
- npm install -i
- npm run build
- npm run dev

backend accessible on http://0.0.0.0:5000
frontend accessible on http://0.0.0.0:8080

#### Testing for production.

In root directory
- docker-compose build --no-cache
- docker-compose up

backend accessible on http://0.0.0.0:5000
frontend accessible on http://0.0.0.0:8080

#### Deployment to a remote server.

Connection to remote server instance required.
SSH <ip-address> etc...

- (For now) copy files across with scp.
- docker-compose build --no-cache
- docker-compose up

backend accessible on http://<server-ip>:5000
frontend accessible on http://<server-ip>:8080

TODO: make sample github actions file to allow for one click deployment and setup
TODO: comment on nginx.conf to show more detail on configuration options
TODO: setup a fetch call from App.vue to ensure connection (and that db read/write can happen from frontend)
TODO: include gunicorn server option as well as flask development server
TODO: create a sample .env file
