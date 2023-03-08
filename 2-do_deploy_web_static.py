#!/usr/bin/env python3
"""Deploy webstack"""
from fabric.api import *
import os.path
from os import path

env.hosts = ['3.84.158.146', '54.144.239.204']


def do_deploy(archive_path):
    """deploy to server"""
    if path.exists('versions') is False:
        return False
    try:
        f_n = archive_path[archive_path.find('/') + 1:archive_path.find('.')]
        f_y = archive_path[archive_path.find('/') + 1:]
        put(archive_path, "/tmp/")
        run("sudo mkdir -p /data/web_static/releases/{}/".format(f_n))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            f_y, f_n))
        run("sudo rm /tmp/{}".format(f_y))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(f_n, f_n))
        run("sudo rm -rf /data/web_static/releases/{}/web_static".format(f_n))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/\
            /data/web_static/current".format(f_n))
        return True
    except Exception:
        return False
    return False

