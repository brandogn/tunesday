import os
import json
import glob
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from spotify_fetcher import fetch_and_save_playlist
# import qrcode
# from qrcode.image.svg import SvgPathImage
from io import BytesIO
from barcode import Gs1_128
from barcode.writer import SVGWriter

app = Flask(__name__)

def generate_playlist_barcode(playlist_data):
    """
    Generate a unique barcode/QR code for a playlist based on its data
    """
    rv = BytesIO()
    # Use playlist name and date to generate a simple barcode string.
    name = playlist_data.get('name', 'PLAYLIST')
    date = playlist_data.get('timestamp')
    barcode_data = f"{date}{name}".upper().replace(" ", "")
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    barcode_data = "".join(c for c in barcode_data if c in allowed_chars)

    # # Truncate to 20 chars if too long
    # barcode_data = barcode_data[:12]
    rv = BytesIO()
    writer_options = dict(
        background="", foreground="#00ff00", font_size=0, 
        quiet_zone=0.0, module_width=.33, module_height=30.0)
    Gs1_128(barcode_data, writer=SVGWriter()).write(rv, options=writer_options)
    # Convert the BytesIO buffer to a string (SVG is XML)
    rv.seek(0)
    svg_xml = rv.read().decode("utf-8")
    
    unwanted_rect = '<rect width="100%" height="100%" style="fill:"/>'
    svg_xml = svg_xml.replace(unwanted_rect, '')

    return svg_xml

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
    
    return render_template('playlist.html', playlist=playlist_data, barcode=generate_playlist_barcode(playlist_data))

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

@app.errorhandler(404)
def not_found(error):
    """
    Custom 404 Not Found handler
    """
    return render_template('error.html', message="404 Not Found"), 404

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
