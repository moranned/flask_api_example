from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

tasks = [
  {
    'id': 1,
    'title': u'Buy groceries',
    'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
    'done': False
  },
  {
    'id': 2,
    'title': u'Learn Python',
    'description': u'Need to find a good Python tutorial on the web',
    'done': False
  }
]

@auth.get_password
def get_password(username):
  if username == 'ned':
    return 'python'
  return None

@auth.error_handler
def unauthorized():
  return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
  return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
  if not request.json or not 'title' in request.json:
    abort(404)
  task = {
    'id': tasks[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json.get('description', ''),
    'done': False
  }
  tasks.append(task)
  return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>')
@auth.login_required
def get_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
  app.run(debug=True)