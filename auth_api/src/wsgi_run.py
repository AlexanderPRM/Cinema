from gevent import monkey

monkey.patch_all()

from app import app, init_db, init_jwt  # noqa: 402


def wsgi_run():
    init_db(app)
    init_jwt(app)
    return app


gunicorn_run = wsgi_run()
