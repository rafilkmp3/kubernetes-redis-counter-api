from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)

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
    return '', 204

@app.route('/healthz', methods=['GET'])
def liveness_check():
    return jsonify({"status": "alive"}), 200

@app.route('/ready', methods=['GET'])
def readiness_check():
    try:
        redis_client.ping()
        return jsonify({"status": "ready"}), 200
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "not ready", "reason": "Redis connection error"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
