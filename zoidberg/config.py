# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.

import codecs
import configparser
import logging
import os
from pathlib import Path
import openai

log = logging.getLogger(__name__)
config_path = p = Path('data/config.ini')

if not os.path.exists(config_path):
    print("Cannot find data file in /data/data.ini! Trying to load from environment variables... ")
    BOT_TOKEN = os.getenv("PEXL_TOKEN")
    TEST_GUILDS = os.getenv("PEXL_TEST_GUILDS")
    SUBSCRIPTION_KEY = os.getenv("PEXL_SUBSCRIPTION_KEY")
    CONTENT_MODERATOR_ENDPOINT = os.getenv("PEXL_CONTENT_MODERATOR_ENDPOINT")
    CONNURL = os.getenv("PEXL_CONNURL")
    DISABLED_COGS = os.getenv("PEXL_DISABLED_COGS")
    HASTE_URL = os.getenv("PEXL_HASTE_URL")
    ADMIN_ID = os.getenv("PEXL_ADMIN_ID")
    openai.api_key = os.getenv("PEXL_OPENAI_KEY")
    error_channel = int(os.getenv("PEXL_ERROR_CHANNEL"))

else:
    config_file = config_path
    config = configparser.ConfigParser()
    config.read_file(codecs.open(config_file, "r+", "utf-8"))

    def read_config(file=config_file):
        config.read_file(codecs.open(file, "r+", "utf-8"))

    BOT_TOKEN = config.get("Bot", "bot_token")
    TEST_GUILDS = config.get("Bot", "testing_guilds").split(",")
    SUBSCRIPTION_KEY = config.get("AI", "azure_cm_sub_key")
    CONTENT_MODERATOR_ENDPOINT = config.get("AI", "azure_cm_endpoint")

    CONNURL = config.get("DB", "connection_url")
    DISABLED_COGS = config.get("Bot", "disabled_cogs").split(", ")

    HASTE_URL = config.get("API", "hastebin_url")

    ADMIN_ID = config.get("Bot", "admin_ids").split(", ")

    openai.api_key = config.get("AI", "openai_api_key")
    error_channel = int(config.get("Bot", "error_channel"))
