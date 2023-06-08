import logging
import logging.handlers
import os
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a folder for log files
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Create a TimedRotatingFileHandler that rotates logs daily
log_file = os.path.join(logs_folder, datetime.now().strftime('%Y-%m-%d') + '.log')
file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight')
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        # Log the request
        logger.info(f"Request - Method: {request.method}, Path: {request.path}, Data: {request.body}")

    def process_response(self, request, response):
        # Log the response
        logger.info(f"Response - Status: {response.status_code}, Data: {response.content}")

        return response
