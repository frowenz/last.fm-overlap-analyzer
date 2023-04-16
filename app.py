from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from overlap import get_user_top_tracks, find_overlap, write_csv
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

LAST_FM_API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='downloads', filename=filename)

@app.errorhandler(Exception)
def handle_exception(e):
    return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/overlap', methods=['POST'])
def calculate_overlap():
    user1 = request.form['user1']
    user2 = request.form['user2']

    user1_data = get_user_top_tracks(user1, LAST_FM_API_KEY)
    user2_data = get_user_top_tracks(user2, LAST_FM_API_KEY)

    overlap_data = find_overlap(user1_data, user2_data)
    output_filename = f"{user1}_{user2}_overlap_{str(uuid.uuid4())}.csv"
    write_csv(output_filename, overlap_data)

    return jsonify({'filename': output_filename})

if __name__ == '__main__':
    app.run(debug=True)
