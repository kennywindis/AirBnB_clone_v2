#!/usr/bin/python3
'''
    Script distributes an archive to
    web servers through automation to both servers
'''
from fabric.api import *
import os

# Servers's addresses
env.hosts = ['100.26.133.225', '54.162.6.57']


def do_deploy(archive_path):
    '''
        Deploy web static content to web server
    '''
    if os.path.isfile(archive_path) is False:
        return False

    start = 'versions'
    print("Starting deployment")

    try:
        # Get the archive file through the file path
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"

        print("Uploading to /tmp/{}".format(filename))
        # Upload the archive to /tmp/ dir web server
        put(archive_path, "/tmp/{}".format(filename))

        print("Creating directory {}".format(path_no_ext))
        # Create directory on web server
        run("mkdir -p {}".format(path_no_ext))

        # Uncompress the archive to "folder"
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))

        # Delete archive file from web server
        run("rm /tmp/{}".format(filename))

        # Move content of web_static to "folder"
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))

        # Delete the content of web_static
        run("rm -rf {}web_static".format(path_no_ext))

        # Delete symbolic link current on web server
        run("rm -rf {}".format(symlink))

        # Create new link: current and point to new version of code in "folder"
        run("ln -s {} {}".format(path_no_ext, symlink))

        print("New version deployed!")
        return True
    except Exception as err:
        return False
