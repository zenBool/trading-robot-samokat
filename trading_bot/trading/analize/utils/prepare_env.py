#!/usr/bin/env python

import os
import pathlib
from configparser import ConfigParser


def get_api_key(test: bool = True):
    if test:
        key = "api_key"
        secret = "api_secret"
    else:
        key = "key"
        secret = "secret"

    config = ConfigParser()
    config_file_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), "..", "config.ini"
    )
    config.read(config_file_path)
    return config["keys"][key], config["keys"][secret]
