#!/usr/bin/env python
import tokenize
from .utils import StringIO, next

class InterpolationError(tokenize.TokenError): pass

import sys
TEXT_TYPE = 'unicode' if sys.version_info[0] == 2 else 'str'

def interpy_untokenize(tokens):
    parts = []
    prev_row = 1
    prev_col = 0

    for token in tokens:
        ttype, tvalue, tstart, tend, tline = token
        row, col = tstart

        # Add whitespace
        col_offset = col - prev_col
        if col_offset > 0:

            parts.append(" " * col_offset)

        parts.append(tvalue)
        prev_row, prev_col = tend

        if ttype in (tokenize.NL, tokenize.NEWLINE):
            prev_row += 1
            prev_col = 0
    return ''.join(parts)


def inject_tokens(value, start=0):
    level = 0
    quotes = value[:3] if value[:3] == value[0]*3 else value[0]
    interpolation = value.split('#{', 1)
    tokens = []
    if len(interpolation) > 1:
        st, next_st = interpolation
        if st == quotes:
            new_value = '{%s'%(next_st)
        else:
            new_value = '%s%s+{%s'%(st, quotes, next_st)
    else:
        new_value = value
    new_value_lines = new_value.split('\n')
    tokens_iter = tokenize.generate_tokens(StringIO(new_value).readline)
    while 1:
        try:
            token = next(tokens_iter)
        except (StopIteration, tokenize.TokenError) as e:
            break
        ttype, tvalue, tstart, tend, tline = token
        if ttype in (tokenize.NL, tokenize.NEWLINE) and level != 0:
            raise Exception("New lines are not allowed inside interpolation tags #{}")
        token = ttype, tvalue, (tstart[0], tstart[1]+start), (tend[0], tend[1]+start), tline
        if ttype == tokenize.OP and tvalue == '{':
            level += 1
            if level == 1:
                tstart = token[2]
                tokens.extend([(tokenize.NAME, TEXT_TYPE, tstart, (tstart[0]+1, tstart[1]+4), tline),(tokenize.OP, '(', (tstart[0], tstart[1]+4), (tstart[0], tstart[1]+5), tline)])
                continue
        elif ttype == tokenize.OP and tvalue == '}':
            level -= 1
            if level == 0:
                end = tend[1]
                tokens.append((tokenize.OP, ')', tend, (tend[0], tend[1]+1), tline))
                # new line
                searcher = '\n'.join(new_value_lines[tend[0]-1:])
                interpolated_st = searcher[end:-len(quotes)] 
                if interpolated_st:
                    tokens.append((tokenize.OP, '+', (tend[0], tend[1]+1), (tend[0], tend[1]+2), tline))
                    next_string = '%s%s%s'%(quotes, interpolated_st,quotes)
                    tokens.extend(inject_tokens(next_string))
                break
        # print token
        tokens.append(token)

    if level != 0:
        raise InterpolationError("The interpolation '%s' is not balanced"%value)
    if tokens[-1][0] == 0:
        tokens.pop()
    return tokens


def interpy_tokenize(readline):
    last_nw_token = None
    prev_token = None
    tokens = tokenize.generate_tokens(readline)
    while 1:
        try:
            token = next(tokens)
        except (StopIteration, tokenize.TokenError):
            break
        ttype, tvalue, tstart, tend, tline = token
        DOUBLE = '"'
        if (ttype == tokenize.STRING and tvalue[-1] == DOUBLE):
            for s_token in inject_tokens(tvalue, tend[1]):
                yield s_token
        else:
            yield token
