import os
from server import app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
