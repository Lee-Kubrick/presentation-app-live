import eventlet
eventlet.monkey_patch()  # IMPORTANT: Do this before anything else

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

print("Server is starting... Visit http://localhost:5000/")


votes = {}

@app.route('/')
def index():
    return "Server is running."

@socketio.on('submit_vote')
def handle_vote(data):
    user_id = data['user_id']
    choice = data['choice']
    votes[user_id] = choice
    emit('update_votes', votes, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
