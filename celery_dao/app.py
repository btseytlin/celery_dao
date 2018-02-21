import json
from flask import Flask, request, abort, Response, g
from .tasks import add
from .utils import get_db_connection
def create_app():
    app = Flask(__name__)

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = get_db_connection()
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route('/add', methods=['POST'])
    def calculate():
        try:
            a, b = int(request.form.get('a', None)), int(request.form.get('b', None))
            task_id = add.apply((a, b))

            # Notice we do not wait for the task to complete
            # We need to respond immediately or the HTTP request will time out.

            query = f'INSERT INTO results (`task_id`, `result`) VALUES (\'{task_id}\', null)'
            cur = get_db().cursor().execute(query)
            return Response(
                response=json.dumps({"task_id": task_id}))
        except TypeError:
            abort(Response(
                response='Expected int params a, b',
                status=500))

    @app.route('/task/<task_id>', methods=['GET'])
    def get_task_result(task_id):
        task_state = 'In processing'
        task_result = None
        with app.app_context():
            query = f'SELECT task_id, result FROM results WHERE task_id = "{task_id}"' #  begging for sql injection
            cur = get_db().cursor().execute(query)
            rv = cur.fetchall()
            if not rv:
                abort(404)

            result = rv[0]
            task_result = result[1]
            if task_result:
                task_state = 'Done'
        return Response(
            response=json.dumps({'task_id': task_id, 'state': task_state, 'result': task_result}))

    return app