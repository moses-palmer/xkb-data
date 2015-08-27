# coding=utf-8
# xkb-data
# Copyright (C) 2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import ply.yacc
import sys

from . import parser


def read(prompt):
    """Reads a single line of user input.

    :param str prompt: The prompt.

    :return: the user input
    """
    try:
        return raw_input(prompt)
    except NameError:
        return input(prompt)


def exit():
    """Exists the program.
    """
    sys.stdout.write('\n')
    sys.exit()


p = parser(start=sys.argv[1] if len(sys.argv) > 1 else None)


# If non-interactive, parse entire stdin and print it without formatting
if not sys.stdin.isatty():
    print(p.parse(sys.stdin.read()))
    sys.exit(0)


data = ''
while True:
    # Read the data, and allow the user to cancel
    try:
        data += read('xkb-data > ' if not data else '> ') + '\n'
    except KeyboardInterrupt:
        if data:
            print('\nInput cancelled')
            data = ''
            continue
        else:
            exit()

    except EOFError:
        exit()

    # Parse the data, clear the cache and display the parsed value
    try:
        item = p.parse(data.strip())
        data = ''
        print('\n%s\n' % (
            '\n'.join(
                ': %s' % l
                for l in repr(item).splitlines())))

    # Assume incomplete data if the error token is None
    except ply.yacc.GrammarError as e:
        if e.args[1] is None:
            continue
        else:
            print('\n\nInvalid data:\n%s\n\n' % data)
            raise
