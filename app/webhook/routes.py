from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import events

bp = Blueprint('webhook', __name__)

@bp.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    data = {}

    if event_type == 'push':
        data = {
            'author': payload['pusher']['name'],
            'to_branch': payload['ref'].split('/')[-1],
            'timestamp': datetime.utcnow(),
            'action': 'push'
        }

    elif event_type == 'pull_request':
        pr = payload['pull_request']
        if payload['action'] == 'opened':
            data = {
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref'],
                'timestamp': datetime.utcnow(),
                'action': 'pull_request'
            }
        elif payload['action'] == 'closed' and pr['merged']:
            data = {
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref'],
                'timestamp': datetime.utcnow(),
                'action': 'merge'
            }

    if data:
        events.insert_one(data)
        return jsonify({"message": "Event received"}), 200
    return jsonify({"message": "Ignored event"}), 400

@bp.route('/events')
def get_events():
    data = list(events.find().sort("timestamp", -1).limit(10))
    for d in data:
        d['_id'] = str(d['_id'])
        d['timestamp'] = d['timestamp'].strftime("%d %b %Y - %I:%M %p UTC")
    return jsonify(data)

@bp.route('/')
def home():
    return render_template("index.html")



