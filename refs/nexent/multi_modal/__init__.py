import functools
import inspect
import logging
from io import BytesIO
from typing import Any, Callable, List, Optional
import requests

from .utils import (
    UrlType,
    is_url,
    generate_object_name,
    detect_content_type_from_bytes,
    guess_extension_from_content_type,
    parse_s3_url
)

logger = logging.getLogger("multi_modal")