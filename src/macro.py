"""
macro.py
Interpreter for the macro system.
"""

import random
import os
from itertools import takewhile
from copy import deepcopy

COMMENT_TAG = "#"

def prune_line(line):
    return line.replace("\t", "").replace(" ", "")
def split_line(line):
    return line.replace("\t", "").split(" ")
def all_to_int(params):
    for x in range(0, len(params)):
        params[x] = int(params[x])
    return params
def tab_to_spaces(inf):
    return inf.replace("\t", "    ")

def get_cmd(s):
    return split_line(s)[0]
def get_params(s):
    return split_line(s)[1:]
def get_params_ints(s):
    return all_to_int(split_line(s)[1:])

is_tab = '\t'.__eq__

def build_tree(lines):
    lines = iter(lines)
    final_stack = []
    rolls = []
    stack = []
    for line in lines:
        if line.lstrip().rstrip().startswith(COMMENT_TAG):
            continue
        if line == "":
            continue
        indent = len(list(takewhile(is_tab, line)))
        stack[indent:] = [line.lstrip().rstrip()]
        if get_cmd(line) == "roll":
            params = get_params_ints(line)
            rolls.append(params)
        if get_cmd(line) == "drop":
            final_stack.append(deepcopy(stack))
    return rolls, final_stack

def roll(rollranges, stacks):
    rolls = []
    for rollrange in rollranges:
        rolls.append(random.randint(rollrange[0], rollrange[1]))

    loot = []
    for stack in stacks:
        roll_index = 0
        for step in stack:
            if get_cmd(step) == "roll":
                pass
            if get_cmd(step) == "range":
                params = get_params_ints(step)
                if rolls[roll_index] >= params[0] and rolls[roll_index] <= params[1]:
                    roll_index += 1
                    continue
                else:
                    break
            if get_cmd(step) == "drop":
                params = get_params(step)
                loot.append(params)

    return rolls, loot


if __name__ == "__main__":
    macro = open('../example/macro2.txt')
    macro = macro.read().split(os.linesep)
    rolls, loot = roll(*build_tree(macro))
    for x in loot:
        print x
    