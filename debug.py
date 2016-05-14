# Run a test server.
from app import create_app

app = create_app('default')
app.run(host='127.0.0.1', port=5001)
