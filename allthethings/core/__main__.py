#!/usr/bin/env python
from cleo import Application

from allthethings.core import ListRepos

application = Application()
application.add(ListRepos())

if __name__ == '__main__':
    application.run()

