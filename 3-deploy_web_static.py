#!/usr/bin/python3
"""
Script to deploy a static website
"""
from datetime import datetime
from fabric.api import *
from os.path import exists
env.hosts = ['3.84.158.146', '54.144.239.204']


def do_pack():
    """
    Pack file into a .tgz archive
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    local("mkdir -p versions")
    new = local("tar -czvf {} web_static".format(filename))
    if new.succeeded:
        return(filename)
    else:
        return(None)


def do_deploy(archive_path):
    """
    Deployment!
    """
    if exists(archive_path) is False:
        return False

    file_name = archive_path.split('/')[1]
    path = "/data/web_static/releases"
    try:
        put(archive_path, '/tmp/')
        run("mkdir -p {}{}".format(path, file_name[:-4]))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name,
                                               path, file_name[:-4]))
        run("rm /tmp/{}".format(file_name))
        run("mv {}{}/web_static/* {}{}/".format(path, file_name[:-4],
                                                path, file_name[:-4]))
        run("rm -rf {}{}/web_static".format(path, file_name[:-4]))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path,
                                                          file_name[:-4]))
        return True
    except:
        return False


def deploy():
    '''
    DEPLOY!!!!!
    '''
    new = do_pack()
    if not new:
        return False
    success = do_deploy(new)
    return(success)

