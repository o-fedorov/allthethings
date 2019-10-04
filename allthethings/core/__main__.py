#!/usr/bin/env python
from cleo import Application

from allthethings.core import ListProjects, AddProject, RemoveProject

application = Application()
application.add(ListProjects())
application.add(AddProject())
application.add(RemoveProject())

if __name__ == '__main__':
    application.run()

