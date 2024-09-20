from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)

@app.route('/read', methods=['GET'])
def read_counter():
    value = redis_client.get('counter')
    if value is None:
        value = 0
    else:
        value = int(value)
    return jsonify({"counter": value})

@app.route('/write', methods=['POST'])
def increment_counter():
    redis_client.incr('counter')
    new_value = int(redis_client.get('counter'))
    return jsonify({"counter": new_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
