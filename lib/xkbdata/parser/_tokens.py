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

import ply.lex


#: The token names; this list will be populated by :func:`token`
tokens = []


def token(f):
    """Marks a function as a token handler.

    :param callable f: The function. Its name must begin with ``'t_'``.

    :return: f
    """
    if f.__name__.startswith('t_'):
        tokens.append(f.__name__[2:])
    else:
        raise RuntimeError('invalid token name: %s', f.__name__)
    return f


#: A single line comment
t_ignore_SLCOMMENT = r'(\#|//)[^\n]*'


# Ignore whitespace
t_ignore = ' \t'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = ply.lex.lex()
