import os
from server import app


def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
