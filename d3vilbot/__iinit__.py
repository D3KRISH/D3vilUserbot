import heroku3
import os
import sys
import time
#import d3vilbot 
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger

from d3vilbot.clients.session import D2, D3, D4, D5, D3vil, D3vilBot
from d3vilbot.config import Config
from d3vilbot.clients import *

print(sys.path)
StartTime = time.time()
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))


if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)


LOGS = getLogger(__name__)

bot = D3vil
tbot = D3vilBot


if not Config.API_HASH:
    LOGS.warning("Please fill var API_HASH to continue.")
    quit(1)


if not Config.APP_ID:
    LOGS.warning("Please fill var APP_ID to continue.")
    quit(1)


if not Config.BOT_TOKEN:
    LOGS.warning("Please fill var BOT_TOKEN to continue.")
    quit(1)
    
    
# if not Config.BOT_USERNAME:
#     LOGS.warning("Please fill var BOT USERNAME to continue.")
#     quit(1)
    

if not Config.DB_URI:    
    LOGS.warning("Please fill var DATABASE_URL to continue.")
    quit(1)


if not Config.D3VILBOT_SESSION:
    LOGS.warning("Please fill var D3VILBOT_SESSION to continue.")
    quit(1)


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None

