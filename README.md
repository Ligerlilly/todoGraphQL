## Run Locally
* Install external dependencies: python3, pip3, sqlite
* `pip3 install -r requirements.txt`
* `export FLASK_APP=app.py`
* `flask run`
* For now, ensure CORS is disabled

Server should now be running at `localhost:5000`. You change the port by editing `app.run()` in `app.py` (ex: `app.run(port=8000)`)`
