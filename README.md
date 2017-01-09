## Run Locally
* Ensure sqlite is installed
* `export FLASK_APP=app.py`
* `flask run`

Server should now be running at `localhost:5000`. You change the port by editing `app.run()` in `app.py` (ex: `app.run(port=8000)`)