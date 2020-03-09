#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/uni_web')

from website import app as application
application.secret_key = b'\xda\x9a\xfa6\x0b\xf5`\xf8GS\xbb\xca\x9c\xb2\xed\x87\xdc\xf4 \xd6eY\xcf\x82'
