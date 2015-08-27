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
"""
This module contains various utility functions used by both the *AST* package
and the grammar files.
"""

import json


def string_escape(s):
    """Escapes a string and adds quotes to it.

    :param str s: The string to escape.

    :return: an escaped and quoted string
    """
    return json.dumps(s)


def string_unescape(s):
    """Unescapes a quoted string.

    :param str s: The string to unescape.

    :return: an unescaped and unquoted string
    """
    return json.loads(s)
