import time

import redis

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Holla! we have hit <count> times.\n'.format(count)
