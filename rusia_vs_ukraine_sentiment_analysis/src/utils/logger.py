import logging
import logging.config
import yaml

def setup_logging():
    with open("config/logger_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()
logger.info("Logging is configured.")
