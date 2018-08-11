=====
Polls
=====

PollsはWebベースの投票を行うための簡単なDjangoアプリです。

詳細なドキュメントは "docs" ディレクトリにあります。

Quick start
-----------

1. INSTALLED_APPSに`polls`を追加します。::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. `urls.py`にpollsのurlをインクルードします。::

    path('polls/', include('polls.urls')),

3. `python manage.py migrate`コマンドでpollsのモデルを作成します。

4. 開発サーバーが起動するので、`http://127.0.0.1:8000/admin`にて投票を作成してください。

5. `http://127.0.0.1:8000/polls`で作成されているのを確認してください。
