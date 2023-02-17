from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Task {self.title}'

# Task resource
class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return {'id': task.id, 'title': task.title, 'completed': task.completed}

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        task.title = data['title']
        db.session.commit()
        return {'id': task.id, 'title': task.title, 'completed': task.completed}

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204

# Task list resource
class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]

    def post(self):
        data = request.get_json()
        task = Task(title=data['title'])
        db.session.add(task)
        db.session.commit()
        return {'id': task.id, 'title': task.title, 'completed': task.completed}, 201

# Mark task as completed or not completed
class TaskCompletedResource(Resource):
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        task.completed = not task.completed
        db.session.commit()
        return {'id': task.id, 'title': task.title, 'completed': task.completed}

# Add resources to the API
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')
api.add_resource(TaskCompletedResource, '/tasks/<int:task_id>/completed')

if __name__ == '__main__':
    app.run(debug=True)
