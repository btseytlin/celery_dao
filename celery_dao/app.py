import json
import os
from flask import Flask, request, abort, Response, g, url_for
from .celery import worker
from celery_dao import tasks
from .db import init_db, get_session
from .models import Result
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if hasattr(g, 'db_session'):
            g.db_session.close()

    init_db(app.config['SQLALCHEMY_DATABASE_URI'])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if hasattr(g, 'db_session'):
            g.db_session.close()

    @app.route('/add', methods=['POST'])
    def calculate():
        try:
            a, b = int(request.form.get('a', None)), int(request.form.get('b', None))
        except TypeError:
            abort(Response(
                response='Expected int params a, b',
                status=500))
        task_id = worker.send_task('celery_dao.tasks.add', args=(a, b)).id

        # Notice we do not wait for the task to complete
        # We need to respond immediately or the HTTP request will time out.
        session = get_session()
        result = Result(task_id=task_id, result=None)
        session.add(result)
        session.commit()
        return Response(
            response=json.dumps({
                "task_id": task_id,
                "task_url": url_for("get_task_result", _external=True, task_id=task_id)
            })
        )

    @app.route('/task/<task_id>', methods=['GET'])
    def get_task_result(task_id):
        task_state = 'In processing'

        session = get_session()
        result = session.query(Result).filter_by(task_id=task_id).first()
        if not result:
            abort(404)
        if result.result:
            task_state = 'Done'
        return Response(
            response=json.dumps({'task_id': task_id, 'state': task_state, 'result': result.result}))

    return app
