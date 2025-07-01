import os
import uuid
import zipfile
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import threading
import time
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB制限
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# フォルダ作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 処理状況を管理する辞書
processing_status = {}

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_video(input_path, output_folder, session_id):
    """動画を10分ごとに分割する"""
    try:
        processing_status[session_id]['status'] = 'processing'
        processing_status[session_id]['progress'] = 0
        
        # 動画ファイル読み込み
        video = VideoFileClip(input_path)
        duration = video.duration
        segment_duration = 600  # 10分 = 600秒
        
        segments = []
        segment_count = int(duration // segment_duration) + (1 if duration % segment_duration > 0 else 0)
        
        for i in range(segment_count):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, duration)
            
            # 分割された動画を作成
            segment = video.subclip(start_time, end_time)
            segment_filename = f"segment_{i+1:03d}.mp4"
            segment_path = os.path.join(output_folder, segment_filename)
            
            segment.write_videofile(segment_path, codec='libx264', audio_codec='aac')
            segments.append(segment_filename)
            
            # 進捗更新
            progress = int(((i + 1) / segment_count) * 100)
            processing_status[session_id]['progress'] = progress
            
            segment.close()
        
        video.close()
        
        # 処理完了
        processing_status[session_id]['status'] = 'completed'
        processing_status[session_id]['segments'] = segments
        processing_status[session_id]['completed_at'] = datetime.now()
        
        # 自動削除タイマー設定（24時間後）
        timer = threading.Timer(24 * 3600, cleanup_files, args=[session_id])
        timer.start()
        
    except Exception as e:
        processing_status[session_id]['status'] = 'error'
        processing_status[session_id]['error'] = str(e)

def cleanup_files(session_id):
    """ファイルを自動削除する"""
    if session_id in processing_status:
        output_folder = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        del processing_status[session_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if file and allowed_file(file.filename):
        # セッションIDを生成
        session_id = str(uuid.uuid4())
        
        # ファイル保存
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(upload_path)
        
        # 出力フォルダ作成
        output_folder = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(output_folder, exist_ok=True)
        
        # 処理状況初期化
        processing_status[session_id] = {
            'status': 'uploading',
            'progress': 0,
            'segments': [],
            'uploaded_at': datetime.now()
        }
        
        # バックグラウンドで分割処理開始
        thread = threading.Thread(target=split_video, args=[upload_path, output_folder, session_id])
        thread.start()
        
        return jsonify({'session_id': session_id}), 200
    
    return jsonify({'error': '対応していないファイル形式です'}), 400

@app.route('/status/<session_id>')
def get_status(session_id):
    if session_id in processing_status:
        return jsonify(processing_status[session_id])
    return jsonify({'error': 'セッションが見つかりません'}), 404

@app.route('/files/<session_id>')
def get_files(session_id):
    if session_id in processing_status and processing_status[session_id]['status'] == 'completed':
        return jsonify({
            'files': processing_status[session_id]['segments'],
            'session_id': session_id
        })
    return jsonify({'error': 'ファイルの準備ができていません'}), 404

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], session_id, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'ファイルが見つかりません'}), 404

@app.route('/download_zip/<session_id>')
def download_zip(session_id):
    if session_id in processing_status and processing_status[session_id]['status'] == 'completed':
        output_folder = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        zip_path = f"{output_folder}.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in processing_status[session_id]['segments']:
                file_path = os.path.join(output_folder, filename)
                zipf.write(file_path, filename)
        
        return send_file(zip_path, as_attachment=True, download_name=f"split_videos_{session_id}.zip")
    
    return jsonify({'error': 'ファイルの準備ができていません'}), 404

# Vercel用のエントリーポイント
app_instance = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)