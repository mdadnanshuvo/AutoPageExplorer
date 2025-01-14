import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to set up a logger
    Args:
        name (str): The name of the logger.
        log_file (str): The file to write the logs to.
        level (int): The logging level.
    Returns:
        logger: Configured logger.
    """
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    return logger

# Set up the main logger
main_logger = setup_logger('main', 'logs/main.log', logging.DEBUG)