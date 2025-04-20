import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store responses like: { question_index: { user_id: choice } }
responses = {}
current_question = 0

@app.route('/')
def index():
    return "Live Voting Server Running"

@socketio.on('connect')
def handle_connect():
    print("A client connected.")

@socketio.on('submit_vote')
def handle_vote(data):
    user_id = data['user_id']
    choice = data['choice']
    question = data['question']

    if question not in responses:
        responses[question] = {}
    responses[question][user_id] = choice

    # Bundle with question index for presenter filtering
    all_votes = {
        uid: { 'choice': ch, 'question': question }
        for uid, ch in responses[question].items()
    }

    emit('update_votes', all_votes, broadcast=True)

@socketio.on('set_question')
def handle_set_question(q_index):
    global current_question
    current_question = q_index
    emit('set_question', current_question, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
