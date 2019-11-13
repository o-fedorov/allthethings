#!/usr/bin/env python
from cleo import Application

from allthethings.core import ListProjects, AddProject, RemoveProject, Execute

application = Application()
application.add(ListProjects())
application.add(AddProject())
application.add(RemoveProject())
application.add(Execute())

if __name__ == "__main__":
    application.run()
