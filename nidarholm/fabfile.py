from fabric.api import *

import os

env.project_name = 'samklang'

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



