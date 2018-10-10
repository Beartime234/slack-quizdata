import os
import logging.config
import yaml
# Get the current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Set up logging
with open(f"{dir_path}/uploader_config/logging.yml", "rt") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Get the question folder
QUESTION_FOLDER = f"{dir_path}/../questions/"

logger.info(f"Initialized Question Loader")
