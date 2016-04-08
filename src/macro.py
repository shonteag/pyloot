"""
macro.py
Interpreter for the macro system.
"""

import random
import os
from copy import deepcopy
import cStringIO

COMMENT_TAG = "#"

CMD_ROLL = "roll"
CMD_RANGE = "range"
CMD_DROP = "drop"

def strip_line(line):
    return line.lstrip().rstrip()
def strip_comments(macro):
    string = cStringIO.StringIO()
    for line in macro:
        if is_statement(line):
            continue
        string.write(line)
    return string
def split_line(line):
    return strip_line(line).split(" ")
def get_cmd_params(line):
    return split_line(line)[0], split_line(line)[1:]
def is_statement(line):
    if (strip_line(line) != "" and 
        not strip_line(line).startswith(COMMENT_TAG)):
        return True
    return False
def in_range(num, params):
    if num >= int(params[0]) and num <= int(params[1]):
        return True
    return False

def get_level_cmd_params(line):
    level = line.count("\t")
    return level, split_line(line)[0], split_line(line)[1:]

class Node(object):
    def __init__(self, parent, line):
        self.parent = parent
        self.children = []
        self.line = line
        self.level, self.cmd, self.params = \
            get_level_cmd_params(self.line)
        self.value = None

    def is_leaf(self):
        return self.cmd == CMD_DROP

    def eval(self):
        if self.cmd == CMD_ROLL:
            # parent is irrelevant
            self.value = random.randint(int(self.params[0]), int(self.params[1]))
        elif self.cmd == CMD_RANGE:
            # parent will always be roll
            self.value = in_range(self.parent.value, self.params)
        elif self.cmd == CMD_DROP:
            # parent will always be range
            if self.parent.value:
                self.value = self.params
        print strip_line(self.line), "\t\t\t", self.value
        return self.value

    def add_child(self, node):
        self.children.append(node)

class LootTree(object):
    def __init__(self, macro):
        self.macro = macro
        self.root = None
        self.line = "TREE"
        self.loot = []

        self.populate()

    def populate(self):
        print "populating..."
        
        def recurse(parent, depth, source):
            last_line = source.readline().rstrip()
            while last_line:
                tabs, cmd, params = get_level_cmd_params(last_line)
                if tabs < depth:
                    break
                node = Node(parent, last_line)
                if tabs >= depth:
                    parent.add_child(node)
                    last_line = recurse(node, tabs+1, source)
            return last_line

        self.root = Node(self, self.macro.readline().rstrip())
        recurse(self.root, 0, self.macro)

    def eval(self):
        print "generating pathing..."

        def recurse(root):
            root.eval()
            if root.is_leaf():
                self.loot.append(root.value)
            else:
                if root.value is not False:
                    for node in root.children:
                            recurse(node)

        recurse(self.root)
        return self.loot


if __name__ == "__main__":
    macro = open('../example/macro2.txt')

    tree = LootTree(macro)
    loot = tree.eval()

    print "=============="
    for item in loot:
        print item
    