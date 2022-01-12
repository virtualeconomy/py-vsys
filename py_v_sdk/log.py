import sys
from loguru import logger


logger.configure(
    handlers=[
        {"sink": sys.stdout, "serialize": True},
    ]
)

logger.disable("py_v_sdk")
