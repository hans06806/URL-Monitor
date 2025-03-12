from flask import Flask, request, jsonify
from database import SessionLocal, get_db
from models import URL
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route('/urls', methods=['POST'])
def add_url():
    data = request.get_json()
    db: Session = get_db()
    url = URL(url=data['url'])
    db.add(url)
    db.commit()
    return jsonify({"message": "URL added successfully", "id": url.id}), 201

@app.route('/urls', methods=['GET'])
def list_urls():
    db: Session = SessionLocal()
    urls = db.query(URL).all()
    return jsonify([{"id": u.id, "url": u.url} for u in urls])

if __name__ == '__main__':
    app.run(debug=True)
