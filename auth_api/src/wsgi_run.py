from gevent import monkey

monkey.patch_all()

from app import app, init_db, init_jwt, init_redis  # noqa: 402


def wsgi_run():
    init_db(app)
    init_redis(app)
    init_jwt(app)
    return app


gunicorn_run = wsgi_run()
