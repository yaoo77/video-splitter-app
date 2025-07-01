# デプロイメント手順

## 推奨：Railway でのデプロイ

Railwayは最も簡単で確実にPythonアプリをデプロイできます。

### 手順

1. **Railway サイトにアクセス**
   - https://railway.app/ にアクセス
   - GitHubアカウントでサインアップ/ログイン

2. **プロジェクトをデプロイ**
   - "Deploy from GitHub repo" を選択
   - `yaoo77/video-splitter-app` リポジトリを選択
   - Railwayが自動でPythonを検出し、`requirements.txt`を読み込みます

3. **環境変数設定（必要に応じて）**
   - Variables タブで環境変数を設定
   - 特に設定は不要ですが、必要に応じて追加

4. **デプロイ完了**
   - 数分でデプロイが完了し、URLが提供されます

## 代替案1：Render でのデプロイ

1. **Render サイトにアクセス**
   - https://render.com/ にアクセス
   - GitHubアカウントでサインアップ/ログイン

2. **Web Service を作成**
   - "New Web Service" を選択
   - GitHubリポジトリを接続
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## 代替案2：Heroku でのデプロイ

### 前提条件
- Herokuアカウント
- Heroku CLI のインストール

### 手順

1. **Heroku CLI でログイン**
   ```bash
   heroku login
   ```
   ブラウザが開くのでログインを完了

2. **Herokuアプリを作成**
   ```bash
   heroku create video-splitter-app-unique-name
   ```

3. **デプロイ**
   ```bash
   git push heroku master
   ```

### 必要ファイル（既に作成済み）
- `Procfile`: Heroku用の起動設定
- `runtime.txt`: Python バージョン指定
- `requirements.txt`: 依存関係

## 代替案3：ローカル実行

最も確実な方法：

```bash
git clone https://github.com/yaoo77/video-splitter-app.git
cd video-splitter-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

ブラウザで `http://localhost:5000` にアクセス

## トラブルシューティング

### Vercel での問題
- MoviePyが動作しない（サーバーレス環境の制限）
- 大きなファイル処理に不向き

### 推奨デプロイ順序
1. **Railway** (最も簡単)
2. **Render** (無料プランあり)
3. **Heroku** (従来からの定番)
4. **ローカル実行** (最も確実)

## 注意事項

- **ファイルサイズ制限**: 各プラットフォームには異なる制限があります
- **実行時間制限**: 無料プランでは処理時間に制限があります
- **ストレージ**: 一時ファイルは定期的に削除されます

完全な動画分割機能を利用するには、**Railway** または **Render** での デプロイを強く推奨します。