import logging

class Log:
    
    def __init__(self):
        logging.basicConfig(filename='app.log', level=logging.INFO)

    def start(message):
        logging.info(message)

    def end(message):
        logging.info(message)
    
    def fetch_error(error):
        logging.error("Database fetch failed: %s", error)
    
    def update_error(error):
        logging.error("Database update failed: %s", error)
        
    def remove_error(error):
        logging.error("Database remove failed: %s", error)
        
    def check_error(error):
        logging.error("Database check failed: %s", error)
        
