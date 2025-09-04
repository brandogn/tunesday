import os
import json
import glob
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from spotify_fetcher import fetch_and_save_playlist

app = Flask(__name__)

def get_available_dates():
    """
    Get list of available playlist dates from data directory
    """
    if not os.path.exists("data"):
        return []
    
    files = glob.glob("data/playlist_*.json")
    dates = []
    
    for file in files:
        # Extract date from filename (playlist_YYYY-MM-DD.json)
        date_str = os.path.basename(file).replace("playlist_", "").replace(".json", "")
        try: # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
            dates.append(date_str)
        except ValueError:
            continue
    
    return sorted(dates, reverse=True)

def load_playlist_data(date_str):
    """
    Load playlist data for a specific date
    """
    filename = f"data/playlist_{date_str}.json"
    
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

@app.route('/')
def index():
    """
    Homepage - shows list of available dates
    """
    dates = get_available_dates()
    return render_template('index.html', dates=dates)

@app.route('/playlist/<date>')
def playlist(date):
    """
    Display playlist for a specific date
    """
    playlist_data = load_playlist_data(date)
    
    if not playlist_data:
        return render_template('error.html', message=f"Playlist data not found for date: {date}"), 404
    
    return render_template('playlist.html', playlist=playlist_data)

@app.route('/current')
def current():
    """
    Display the most recent playlist (current state)
    """
    dates = get_available_dates()
    
    if not dates:
        return render_template('error.html', message="No playlist data available"), 404
    
    # Redirect to most recent date
    return playlist(dates[0])

@app.errorhandler(404)
def not_found(error):
    """
    Custom 404 Not Found handler
    """
    return render_template('error.html', message="404 Not Found"), 404


# @app.route('/admin/update')
# def admin_update():
#     """
#     Admin endpoint to manually update playlist data
#     """
#     result = fetch_and_save_playlist()
    
#     if result['success']:
#         return jsonify({
#             'status': 'success',
#             'message': f"Playlist updated successfully. {result['total_tracks']} tracks saved.",
#             'date': result['date'],
#             'filename': result['filename']
#         })
#     else:
#         return jsonify({
#             'status': 'error',
#             'message': f"Failed to update playlist: {result['error']}"
#         }), 500

# @app.route('/api/playlist/<date>')
# def api_playlist(date):
#     """
#     API endpoint to get playlist data as JSON
#     """
#     playlist_data = load_playlist_data(date)
    
#     if not playlist_data:
#         return jsonify({'error': 'Playlist not found'}), 404
    
#     return jsonify(playlist_data)

# @app.route('/api/dates')
# def api_dates():
#     """
#     API endpoint to get list of available dates
#     """
#     dates = get_available_dates()
#     return jsonify({'dates': dates})

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
