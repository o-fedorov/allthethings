#!/usr/bin/env python
from cleo import Application

from allthethings.core import AddProject, Execute, ListProjects, RemoveProject

application = Application()
application.add(ListProjects())
application.add(AddProject())
application.add(RemoveProject())
application.add(Execute())

if __name__ == "__main__":
    application.run()
