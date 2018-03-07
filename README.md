## Run Locally
* Install external dependencies: python3, pip3, sqlite
* `pip3 install -r requirements.txt`
* `export FLASK_APP=app.py`
* `python3 -m flask run`
* For now, ensure browser CORS are disabled

Server should now be running at `localhost:5000`. You change the port by editing `app.run()` in `app.py` (ex: `app.run(port=8000)`)

Visit `localhost:5000/graphql` and enter the following query
'''
{
    allTodoLists {
        edges {
            node {
                id
                name
                todos {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
        }
    }
}
'''
then hit the play button