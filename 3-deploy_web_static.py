#!/usr/bin/python3
"""Deploy"""
from fabric.api import local
from fabric.api import env
from fabric.operations import run, put
from datetime import datetime
import os.path
from os import path


do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ['34.75.185.85', '34.73.88.228']


def deploy():
    """deploy"""
    path_name = do_pack()
    if not path_name:
        return False

    value = do_deploy(path_name)
    return value
