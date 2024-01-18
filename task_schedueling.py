from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import itertools

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    task_details = db.Column(db.String(255), nullable=False)


@app.route('/schedule_task', methods=['POST'])
def schedule_task():
    try:
        task_data = request.json
        task_name = task_data.get('task_name')
        task_details = task_data.get('task_details')
        new_task = Task(task_name=task_name, task_details=task_details)
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.id
        worker_nodes = ['worker1', 'worker2', 'worker3']
        selected_worker = round_robin(worker_nodes)
        response_data = {'status': 'success', 'message': 'Task scheduled successfully', 'task_id': task_id,
                         'worker_node': selected_worker}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


def round_robin(iterable):
    iters = [iter(it) for it in iterable]
    while iters:
        for it in iters[:]:
            try:
                yield next(it)
            except StopIteration:
                iters.remove(it)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
