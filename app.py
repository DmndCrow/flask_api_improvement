import os

from api import create_app
from dotenv import load_dotenv

load_dotenv()

port = os.getenv('FLASK_PORT')
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
