from app import app
from config import DEBUG, PORT
from utils.db import db
from utils.utils import log

try:
    with app.app_context():
        import models
        db.create_all()
except Exception as e:
    log(f"Error al conectar con la base de datos: {e}")
    exit()

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)