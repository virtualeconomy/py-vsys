"""
log contains logger initialization operations.
"""
import sys
from loguru import logger


logger.configure(
    handlers=[
        {"sink": sys.stdout, "serialize": True},
    ]
)

logger.disable("py_vsys")
