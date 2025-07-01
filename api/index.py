from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# HTMLテンプレート
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>動画10分分割ツール - Vercel版</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .limitation-notice {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 30px;
        }
        .limitation-notice h3 {
            color: #856404;
            margin-top: 0;
        }
        .limitation-notice p {
            color: #856404;
            margin-bottom: 0;
        }
        .features {
            margin: 30px 0;
        }
        .feature-list {
            list-style: none;
            padding: 0;
        }
        .feature-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .feature-icon {
            font-size: 24px;
            margin-right: 15px;
            width: 30px;
        }
        .setup-section {
            background-color: #e9ecef;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
        }
        .setup-section h3 {
            margin-top: 0;
            color: #495057;
        }
        .code-block {
            background-color: #212529;
            color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Monaco', 'Consolas', monospace;
            overflow-x: auto;
            margin: 10px 0;
        }
        .github-link {
            text-align: center;
            margin: 30px 0;
        }
        .github-button {
            display: inline-block;
            padding: 12px 30px;
            background-color: #24292e;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .github-button:hover {
            background-color: #1a1e22;
        }
        .alternative-solutions {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
        }
        .alternative-solutions h3 {
            color: #155724;
            margin-top: 0;
        }
        .solution-item {
            margin: 15px 0;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        .solution-item h4 {
            margin-top: 0;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 動画10分分割ツール</h1>
        
        <div class="limitation-notice">
            <h3>⚠️ Vercelでの制限について</h3>
            <p>Vercelのサーバーレス環境では、MoviePyのような重い動画処理ライブラリが動作しません。</p>
            <p>完全な機能を利用するには、以下の代替方法をご利用ください。</p>
        </div>
        
        <div class="alternative-solutions">
            <h3>🚀 推奨デプロイ方法</h3>
            
            <div class="solution-item">
                <h4>1. Railway (推奨)</h4>
                <p>Pythonアプリケーションに最適で、MoviePyも動作します。</p>
                <div class="code-block">
# GitHubと連携してワンクリックデプロイ
https://railway.app/
</div>
            </div>
            
            <div class="solution-item">
                <h4>2. Render</h4>
                <p>無料プランでもPythonアプリケーションをデプロイできます。</p>
                <div class="code-block">
# requirements.txtを自動認識
https://render.com/
</div>
            </div>
            
            <div class="solution-item">
                <h4>3. Heroku</h4>
                <p>従来からある安定したPythonホスティングサービス。</p>
                <div class="code-block">
# Procfileを追加してデプロイ
echo "web: python app.py" > Procfile
</div>
            </div>
            
            <div class="solution-item">
                <h4>4. ローカル実行</h4>
                <p>最も確実で高速な方法です。</p>
                <div class="code-block">
git clone https://github.com/yaoo77/video-splitter-app.git
cd video-splitter-app
pip install -r requirements.txt
python app.py
</div>
            </div>
        </div>
        
        <div class="features">
            <h2>✨ 完全版の機能</h2>
            <ul class="feature-list">
                <li class="feature-item">
                    <span class="feature-icon">📤</span>
                    <span>動画ファイル（MP4, MOV, AVI）のアップロード（最大2GB）</span>
                </li>
                <li class="feature-item">
                    <span class="feature-icon">✂️</span>
                    <span>自動で10分ごとに動画を分割</span>
                </li>
                <li class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span>リアルタイムの処理進捗表示</span>
                </li>
                <li class="feature-item">
                    <span class="feature-icon">💾</span>
                    <span>個別ファイルまたはZIP一括ダウンロード</span>
                </li>
                <li class="feature-item">
                    <span class="feature-icon">🗑️</span>
                    <span>24時間後の自動ファイル削除</span>
                </li>
            </ul>
        </div>
        
        <div class="setup-section">
            <h3>🛠️ ローカル環境でのセットアップ</h3>
            <div class="code-block">
# 1. リポジトリをクローン
git clone https://github.com/yaoo77/video-splitter-app.git
cd video-splitter-app

# 2. 仮想環境を作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 3. 依存関係をインストール
pip install -r requirements.txt

# 4. アプリケーションを起動
python app.py
            </div>
            <p>起動後、ブラウザで <code>http://localhost:5000</code> にアクセスしてください。</p>
        </div>
        
        <div class="github-link">
            <a href="https://github.com/yaoo77/video-splitter-app" class="github-button" target="_blank">
                📚 GitHub でソースコードを見る
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d;">
            <p>© 2025 Video Splitter App - 完全版はローカル環境またはRailway/Renderでご利用ください</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Vercel deployment is working'})

# Vercelハンドラー
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True)