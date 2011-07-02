from fabric.api import *

import os

env.project_name = 'nidarholm'

# environments
def hylla():
    """Sigurd's server setup.

    Usage: fab hylla deploy
    """

    env.installation = "hylla"
    env.hosts = ["sigurdga.no"]
    env.path = "/srv/www/nidarholm"

def setup():
    """Command to setup the environment on the server. Needs more access than deploy"""

    require("hosts")
    require("path")

    sudo("apt-get install -y python-setuptools libapache2-mod-wsgi memcached gcc python-dev")
    sudo("pip install virtualenv")
    sudo("mkdir -p %(path)s" % env)
    with cd(env.path):
        run("virtualenv .")
        run("mkdir releases; mkdir shared; mkdir packages")

def deploy():
    require('hosts')
    require('installation')

    import time
    env.tag_name = "%(installation)s-" % env + time.strftime('%Y-%m-%d-%H-%M-%S')
    env.installation_path = "%(path)s/releases/%(tag_name)s/%(project_name)s" % env
    env.project_path = "%(path)s/releases/%(tag_name)s/%(project_name)s/%(project_name)s" % env
    #upload_apps() or
    push_project()
    install_requirements()
    #deploy_static()
    install_site()
    symlink_current_release()
    restart_webserver()

def git_tag():
    require('tag_name', provided_by=[deploy])
    local("git tag %(tag_name)s" % env)

def push_project():
    require('tag_name', provided_by=[deploy])
    require('installation_path', provided_by=[deploy])
    git_tag()
    local('cd .. && git archive --format=tar --output=%(tag_name)s.tar %(tag_name)s' % env)
    run("mkdir -p %(installation_path)s" % env)
    put("../%(tag_name)s.tar" % env, "%(path)s/packages/" % env)
    with cd(env.installation_path):
        run("tar xf ../../../packages/%(tag_name)s.tar" % env)
    local("cd .. && rm %(tag_name)s.tar" % env)

def install_requirements():
    require('path', provided_by=[deploy])
    require('project_path', provided_by=[deploy])
    with cd(env.path):
        run("pip uninstall -y -E . -r %(project_path)s/uninstall.txt" % env)
        run("pip install -E . -r %(project_path)s/requirements.txt" % env)

def install_site():
    """Needs an apache virtualenv config file with the same name as the local env var "installation"."""

    require("project_path", provided_by=[push_project])
    sudo('ln -sf %(project_path)s/config/%(installation)s.apache.conf /etc/apache2/sites-available/%(project_name)s' % env)
    sudo('a2ensite %(project_name)s' % env)

def symlink_current_release():
    require("tag_name", provided_by=[deploy])
    with cd(env.path):
        run('test -e releases/previous && rm releases/previous || echo "no previous deploy found"')
        run('test -e releases/current && mv releases/current releases/previous || echo "no current deploy found"')
        run('ln -s %(tag_name)s releases/current' % env, pty=True)

def deploy_static():
    require("project_path", provided_by=[push_project])
    with cd(env.project_path):
        run('%(path)s/bin/python manage.py collectstatic -v0 --noinput' % env)

def restart_webserver():
    sudo("/etc/init.d/apache2 reload")


# convenience commands for git
def pull():
    """Pull all repos under ../s7n"""

    main_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.join(main_dir, "..", "s7n")
    dirs = os.listdir(repo_dir)
    for _dir in dirs:
        path = os.path.join(repo_dir, _dir)
        if os.path.isdir(path):
            local('cd %s; git pull' % path)
    local('git pull')

def status():
    """Run git status on all repos under ../s7n"""
    main_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.join(main_dir, "..", "s7n")
    dirs = os.listdir(repo_dir)
    for _dir in dirs:
        path = os.path.join(repo_dir, _dir)
        if os.path.isdir(path):
            local('cd %s; git status' % path)
    local('git status')



