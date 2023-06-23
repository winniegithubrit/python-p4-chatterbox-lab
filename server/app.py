from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        return jsonify([message.to_dict() for message in messages])

    if request.method == 'POST':
        data = request.get_json()
        if 'username' not in data or 'body' not in data:
            return jsonify({'error': 'Missing username or body'}), 200

        message = Message(username=data['username'], body=data['body'])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = db.session.get(Message, id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        for attr, value in data.items():
            setattr(message, attr, value)
        db.session.commit()
        return jsonify(message.to_dict()), 200

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5555)
