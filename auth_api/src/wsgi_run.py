from gevent import monkey

monkey.patch_all()

from app import app, init_db  # noqa: 402

if __name__ == "__main__":
    init_db(app)
