from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)
API_TOKEN = "supersecrettoken123"
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

@app.route('/api/time', methods=['GET'])
@token_required
def get_city_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Please provide a city parameter"}), 400

    city = city.strip().title()

    city_timezones = {
        "Washington": "America/New_York",
        "London": "Europe/London",
        "Tokyo": "Asia/Tokyo",
        "Delhi": "Asia/Kolkata",
        "Canberra": "Australia/Sydney",
        "Ottawa": "America/Toronto"
    }

    if city not in city_timezones:
        return jsonify({"error": f"City '{city}' not found in our database."}), 404

    timezone = pytz.timezone(city_timezones[city])
    now = datetime.now(timezone)
    offset = now.strftime('%z')
    utc_offset = f"{offset[:3]}:{offset[3:]}"
    local_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "city": city,
        "local_time": local_time,
        "utc_offset": utc_offset
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
