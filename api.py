from flask import Flask, request, jsonify, send_from_directory
import os
import time
import yt_dlp
import uuid
import subprocess
import platform

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = 'downloads'

def delete_old_files():
    time_threshold = 120  # 2 minutes in seconds

    current_time = time.time()

    for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):
        if filename.endswith('.mp4') or filename.endswith('.webm'):
            file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            try:
                creation_time = os.path.getctime(file_path)
                if (current_time - creation_time) > time_threshold:
                    os.remove(file_path)
                    print(f"File '{filename}' has been deleted.")
            except Exception as e:
                print(f"Error removing file '{filename}': {str(e)}")

def download_using_gallerydl(url, videoRandomID):
    cmd_line = ['gallery-dl']
    cmd_line += ['--verbose']
    cmd_line += ['--cookies', os.getcwd() + '/cookies.txt']
    cmd_line += ['--ignore-config']
    cmd_line += ["-c", os.getcwd() + "/gallery-dl.conf"]
    cmd_line += ['--directory', os.getcwd() + '/' + app.config['DOWNLOAD_FOLDER']]
    cmd_line += ['--filename', videoRandomID + '.webm']
    cmd_line += ['--ugoira-conv-lossless']
    cmd_line += ['-o', 'signals-ignore=SIGTTOU,SIGTTIN']
    cmd_line += [url]

    if platform.system() == 'Windows':
        popen = subprocess.Popen(cmd_line, text = True, creationflags = subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        popen = subprocess.Popen(cmd_line, text = True, preexec_fn = os.setpgrp)

    popen.wait()
    
    return check_gallerydl_return_code(popen.returncode)
    
def check_gallerydl_return_code(code: int):
    errors = []
    if code & 1: errors.append("unspecified error")
    if code & 2: errors.append("cmdline arguments")
    if code & 4: errors.append("http error")
    if code & 8: errors.append("not found / 404")
    if code & 16: errors.append("auth / login")
    if code & 32: errors.append("format or filter")
    if code & 64: errors.append("no extractor")
    if code & 128: errors.append("os error")
    return ", ".join(errors)

def download_using_ytdlp(url, videoRandomID):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt',
        'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], videoRandomID + '.mp4')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET'])
def index():
    return 'running ✅'

@app.route('/get_video', methods=['GET'])
def get_tweet_video():
    delete_old_files()
    video_url = request.args.get('url')
    videoRandomID = str(uuid.uuid4()).rsplit('-', 1)[-1] #todo: generate from url so already downloaded files are reused

    if video_url:
        if 'twitter.com' not in video_url and 'https://www.pixiv.net/en/artworks/' not in video_url:
            return jsonify({'error': 'twitter.com or pixiv.net artwork url is expected'})
        try:
            ext = 'mp4'
            if 'https://www.pixiv.net/en/artworks/' in video_url:
                gdl_result = download_using_gallerydl(video_url, videoRandomID)
                if gdl_result:
                    raise Exception(f"Gallery-dl failed: {gdl_result}")
                ext = 'webm'
            else:
                download_using_ytdlp(video_url, videoRandomID)
                
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], f'{videoRandomID}.{ext}')
        except Exception as err:
            print(err)
            return jsonify({'error': 'error while downloading video', 'error_details': str(err)}), 400
    else:
        return jsonify({'error': 'Invalid url'}), 500

if __name__ == '__main__':
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])
    app.run(host="0.0.0.0", port=5000)
