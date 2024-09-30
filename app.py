from flask import Flask, render_template, jsonify, request
from flask_caching import Cache
import json
import logging

app = Flask(__name__)

# Setup caching configuration
app.config['CACHE_TYPE'] = 'SimpleCache' 
cache = Cache(app)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

def load_scores():
    try:
        with open('scores.json', 'r') as file:
            data = json.load(file)
        logging.info("Scores loaded successfully.")
        return data
    except FileNotFoundError:
        logging.error("The scores file was not found.")
        return []
    except json.JSONDecodeError:
        logging.error("JSON Decode Error - the file might be corrupted.")
        return []

def process_leaderboard(data, query=None, page=1, per_page=20):
    filtered_leaderboard = {}
    for user_data in data:
        name = user_data['name']
        scores = sorted([sub['score'] for sub in user_data['submissions']], reverse=True)[:24]
        if len(scores) >= 3:
            user_total_score = sum(scores)
            if query and (query.lower() in name.lower() or str(user_total_score) == query):
                filtered_leaderboard[name] = user_total_score
            elif not query:
                filtered_leaderboard[name] = user_total_score

    sorted_leaderboard = sorted(filtered_leaderboard.items(), key=lambda x: x[1], reverse=True)
    start = (page - 1) * per_page
    end = start + per_page
    return sorted_leaderboard[start:end]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/leaderboard')
@cache.cached(timeout=300, query_string=True)
def api_leaderboard():
    query = request.args.get('query')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)
    data = load_scores()
    if data:
        leaderboard = process_leaderboard(data, query=query, page=page, per_page=per_page)
        return jsonify(leaderboard)
    else:
        return jsonify({"error": "Failed to load scores"}), 500

if __name__ == '__main__':
    app.run(debug=True)

