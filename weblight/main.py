# Run a test server.
from app import create_app

app = create_app('production')
app.run(host='0.0.0.0', port=5001)
