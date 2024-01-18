import web_server
from web_server import db
with web_server.app_context():
    db.create_all()

