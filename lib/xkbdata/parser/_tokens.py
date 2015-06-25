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
import re


from xkbdata._util import string_unescape


precedence = (
    ('right', 'EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXCLAM', 'INVERT'),
    ('left', 'OPAREN'))


#: The token names; this list will be populated by :func:`token`
tokens = []


#: The symbols
symbols = {
    '=': 'EQUALS',
    '+': 'PLUS',
    '-': 'MINUS',
    '/': 'DIVIDE',
    '*': 'TIMES',
    '{': 'OBRACE',
    '}': 'CBRACE',
    '(': 'OPAREN',
    ')': 'CPAREN',
    '[': 'OBRACKET',
    ']': 'CBRACKET',
    '.': 'DOT',
    ',': 'COMMA',
    ';': 'SEMI',
    '!': 'EXCLAM',
    '~': 'INVERT'
}

globals().update(
    ('t_' + v, re.escape(k))
    for k, v in symbols.items())
tokens.extend(symbols.values())


#: The reserved words
reserved = {
    'action': 'ACTION',
    'alias': 'ALIAS',
    'alphanumeric_keys': 'ALPHANUMERIC_KEYS',
    'alternate': 'ALTERNATE',
    'alternate_group': 'ALTERNATE_GROUP',
    'augment': 'AUGMENT',
    'default': 'DEFAULT',
    'function_keys': 'FUNCTION_KEYS',
    'group': 'GROUP',
    'hidden': 'HIDDEN',
    'include': 'INCLUDE',
    'indicator': 'INDICATOR',
    'interpret': 'INTERPRET',
    'key': 'KEY',
    'keypad_keys': 'KEYPAD_KEYS',
    'keys': 'KEYS',
    'logo': 'LOGO',
    'modifier_keys': 'MODIFIER_KEYS',
    'mod_map': 'MODIFIER_MAP',
    'modifier_map': 'MODIFIER_MAP',
    'modmap': 'MODIFIER_MAP',
    'outline': 'OUTLINE',
    'overlay': 'OVERLAY',
    'override': 'OVERRIDE',
    'partial': 'PARTIAL',
    'replace': 'REPLACE',
    'row': 'ROW',
    'section': 'SECTION',
    'shape': 'SHAPE',
    'solid': 'SOLID',
    'text': 'TEXT',
    'type': 'TYPE',
    'virtual': 'VIRTUAL',
    'virtual_modifiers': 'VIRTUAL_MODIFIERS',
    'xkb_compat': 'XKB_COMPATMAP',
    'xkb_compat_map': 'XKB_COMPATMAP',
    'xkb_compatibility': 'XKB_COMPATMAP',
    'xkb_compatibility_map': 'XKB_COMPATMAP',
    'xkb_geometry': 'XKB_GEOMETRY',
    'xkb_keycodes': 'XKB_KEYCODES',
    'xkb_keymap': 'XKB_KEYMAP',
    'xkb_layout': 'XKB_LAYOUT',
    'xkb_semantics': 'XKB_SEMANTICS',
    'xkb_symbols': 'XKB_SYMBOLS',
    'xkb_types': 'XKB_TYPES'
}

tokens.extend(reserved.values())


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


#: A general identifier
@token
def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    # Make sure that this wildcard matcher does not shadow reserved words;
    # reserved words are case-insensitive; they may appear as field names as
    # well, so we need to retry in some cases in xkbdata.parser.grammar.p_error
    t.type = reserved.get(t.value.lower(), 'ID')

    return t


#: A key name
@token
def t_KEYNAME(t):
    r'<([^\s]+)>'
    # Strip the brackets
    t.value = t.value[1:-1]

    return t


#: A floating point literal
@token
def t_FLOATLIT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


#: A hex literal
@token
def t_HEXLIT(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t


#: A decimal literal
@token
def t_DECLIT(t):
    r'\d+'
    t.value = int(t.value)
    return t


#: A string literal
@token
def t_STRINGLIT(t):
    r'"(\\"|[^"])*?"'
    t.value = string_unescape(t.value)
    return t


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
