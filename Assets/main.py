from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    spotify_link = request.form['spotify_link']

    # Ensure the 'download' directory exists
    if not os.path.exists('download'):
        os.makedirs('download')

    # Download the song using SpotDL
    command = f"spotdl {spotify_link} --output ./download/"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors during SpotDL download
    if result.returncode != 0:
        return f"Error downloading song: {result.stderr.decode()}"

    # Find the latest downloaded audio file in the download folder
    downloaded_files = [f for f in os.listdir('./download') if f.endswith(('.mp3', '.m4a', '.flac'))]
    if not downloaded_files:
        return "Download failed. No song was downloaded."

    song_file = max(downloaded_files, key=lambda f: os.path.getctime(os.path.join('./download', f)))

    # Send the song file to the user
    return send_file(os.path.join('./download', song_file), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
