#!/usr/bin/env python

import sys


def main(content_file):
    with open('template.html', 'r') as f:
        template = f.read()
    with open(content_file, 'r') as f:
        content = f.read()
    with open('presentation.html', 'w') as f:
        f.write(template.replace('<!-- REPLACEME -->', content))

if __name__ == '__main__':
    main(sys.argv[1])
