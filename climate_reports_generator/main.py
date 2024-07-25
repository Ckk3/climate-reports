import logging
from socketserver import TCPServer, BaseRequestHandler

from database import setup_database
from utils import add_new_user
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class TCPHandler(BaseRequestHandler):
    def handle(self):
        # Handle requests with clients info
        data = self.request.recv(1024).decode('utf-8').strip()
        logger.info(f"Data received: {data}")
        try:
            # Add new user to db
            add_new_user(data=data)
            self.request.send('Ok'.encode('utf-8'))
        except Exception as e:
            self.request.send(str(e).encode('utf-8'))


if __name__ == "__main__":
    logger.info("Setup database")
    setup_database()
    
    logger.info("Starting TCP Server")
    HOST, PORT = "0.0.0.0", 5784

    server = TCPServer((HOST, PORT), TCPHandler)
    logger.info(f"Server running in {HOST}:{PORT}...")
    server.serve_forever()
