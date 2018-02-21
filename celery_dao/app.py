import json
from flask import Flask, request, abort, Response, g
from .celery import worker
from celery_dao import tasks
import os
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    from .models import db, Result
    db.init_app(app)

    with app.app_context():
        db.create_all()

    def celery_worker():
        return worker

    @app.route('/add', methods=['POST'])
    def calculate():
        try:
            a, b = int(request.form.get('a', None)), int(request.form.get('b', None))
        except TypeError:
            abort(Response(
                response='Expected int params a, b',
                status=500))
        task_id = celery_worker().send_task('celery_dao.tasks.add', args=(a, b)).id

        # Notice we do not wait for the task to complete
        # We need to respond immediately or the HTTP request will time out.

        result = Result(task_id=task_id, result=None)
        db.session.add(result)
        db.session.commit()

        print('all results', Result.query.all())
        return Response(response=json.dumps({"task_id": task_id}))


    @app.route('/task/<task_id>', methods=['GET'])
    def get_task_result(task_id):
        task_state = 'In processing'

        result = Result.query.filter_by(task_id=task_id).first()
        if not result:
            abort(404)
        if result.result:
            task_state = 'Done'
        return Response(
            response=json.dumps({'task_id': task_id, 'state': task_state, 'result': result.result}))

    return app