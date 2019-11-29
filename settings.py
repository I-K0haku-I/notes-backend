from settings_dev import *

try:
    from settings_prod import *
except ImportError:
    pass