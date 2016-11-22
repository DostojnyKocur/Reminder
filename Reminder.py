#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Application start point.
"""

import sys
from src.Application import Application


def main():
    """
    Main function.
    """
    result = Application.run(sys.argv)
    sys.exit(result)

# Application start point.
if __name__ == '__main__':
    main()



