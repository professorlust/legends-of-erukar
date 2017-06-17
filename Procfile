web: gunicorn --worker-class eventlet -w 1 serve:app
worker: gunicorn serve:app -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:$PORT --reload
