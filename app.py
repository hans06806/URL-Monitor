from flask import Flask, request, jsonify
from database import SessionLocal, get_db
from models import URL
from sqlalchemy.orm import Session

# Flask imports (Flask, request, jsonify)
# Database imports (SessionLocal, get_db) local imports databease.py
# Model imports (URL) local imports models.py
# SQLAlchemy imports (Session)

app = Flask(__name__) # initialize Flask app, __name__ is the name of the current module
# __name__ is a built-in variable which evaluates to the name of the current module.
# This variable is used to determine if the script is being run on its own or being imported.

@app.route('/urls', methods=['POST']) # route() decorator is used to bind a function to a URL
def add_url():
    data = request.get_json() # get_json() method is used to parse the incoming JSON request data
    db: Session = next(get_db()) # get_db() returns a generator, next() is used to get the first element
    url = URL(url=data['url']) # create a new URL object
    db.add(url) # add the URL object to the session
    db.commit() # commit the transaction
    return jsonify({"message": "URL added successfully", "id": url.id}), 201

@app.route('/urls', methods=['GET'])
def list_urls():
    db: Session = SessionLocal()
    urls = db.query(URL).all() # query all URLs curently in the URL table
    return jsonify([{"id": u.id, "url": u.url} for u in urls])
    # return a JSON response with the list of URLs
    # For each element u in the urls iterable, this part creates a Python dictionary.

if __name__ == '__main__': 
    app.run(debug=True)
    #Ensures the Flask application runs only when the script is executed directly, not imported as a module.
