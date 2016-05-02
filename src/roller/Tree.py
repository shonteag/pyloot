"""
macro.py
Interpreter for the macro system.

The interpreter returns a list of lists.
[["loot", "key", "1"], ...]
The internal lists are constructed from
macro files, and detail the loot keys
provided in said file.

Entry:
-------
from pyloot.roller.Tree import LootTree
tree = LootTree("path/to/macro/file")
loot_keys = tree.eval()
-------
"""

import random
import os
from copy import deepcopy
import cStringIO

COMMENT_TAG = "#"

CMD_ROLL = "roll"
CMD_RANGE = "range"
CMD_DROP = "drop"

# utilities
def strip_line(line):
    return line.lstrip().rstrip()
def split_line(line):
    return strip_line(line).split(" ")
def get_next_line(macro):
    line = macro.readline().rstrip()
    while is_comment(line):
        if not line:
            break
        line = macro.readline().rstrip()
    return line

def get_cmd_params(line):
    return split_line(line)[0], split_line(line)[1:]
def get_level_cmd_params(line):
    level = line.count("\t")
    return level, split_line(line)[0], split_line(line)[1:]

def is_comment(line):
    if (strip_line(line) == "" or 
        strip_line(line).startswith(COMMENT_TAG)):
        return True
    return False
def in_range(num, params):
    if num >= int(params[0]) and num <= int(params[1]):
        return True
    return False


class _Node(object):
    """
    A node in the LootTree. Points to
    parent and has list of pointers to
    children.
    """
    def __init__(self, parent, line):
        self.parent = parent
        self.children = []
        self.line = line
        self.level, self.cmd, self.params = \
            get_level_cmd_params(self.line)
        self.value = None

    def is_leaf(self):
        """
        All leaves are of type DROP.
        """
        return self.cmd == CMD_DROP

    def eval(self):
        """
        eval() performs different actions
        depending on the cmd to which it is
        keyed.
        """
        if self.cmd == CMD_ROLL:
            # parent is irrelevant
            self.value = random.randint(
                int(self.params[0]), int(self.params[1]))
        elif self.cmd == CMD_RANGE:
            # parent will always be roll
            self.value = in_range(self.parent.value,
                                  self.params)
        elif self.cmd == CMD_DROP:
            # parent will always be range
            if self.parent.value:
                self.value = self.params
        return self.value

    def add_child(self, node):
        """
        Add a child to the nodes internal
        children list.
        """
        self.children.append(node)

class LootTree(object):
    """
    Main entry point for this module.
    Takes an open macro file handler
    as input, and parses into a rollable
    loot table.
    A roll can be made using LootTree.eval()
    """
    def __init__(self, macro):
        self.macro = macro
        self.root = None
        self.leaves = []
        self.line = "TREE"
        self.loot = []

        self._populate()

    def _populate(self):
        """
        Internal method.
        Constructs the tree structure based
        on the supplied macro file.
        """
        def recurse(parent, depth, source):
            last_line = get_next_line(source)
            while last_line:
                tabs, cmd, params = get_level_cmd_params(last_line)
                if tabs < depth:
                    break
                node = _Node(parent, last_line)
                if tabs >= depth:
                    parent.add_child(node)
                    last_line = recurse(node, tabs+1, source)
                if node.is_leaf():
                    self.leaves.append(node)
            return last_line

        self.root = _Node(self, get_next_line(self.macro))
        # reset the macrofile handler
        recurse(self.root, 0, self.macro)

    def eval(self):
        """
        Used to perform a loot roll on the
        constructed loot table, and returns
        list of 'dropped' loot as macro-
        specified keys of type list.
        """
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

    def eval_dropchance(self):
        """
        Evaluate the drop chance at each
        of the DROP nodes (leaves) and return
        a dict keyed to the parameter string
        of each DROP node.
        """
        drop_chances = {}
        for leaf in self.leaves:
            last_range = 0
            chance = 1
            node = leaf
            while True:
                if node.cmd == CMD_RANGE:
                    last_range = int(node.params[1]) + 1 - int(node.params[0])
                if node.cmd == CMD_ROLL:
                    roll_range = int(node.params[1]) + 1 - int(node.params[0])
                    roll_chance = float(last_range) / float(roll_range)
                    chance *= roll_chance
                
                if node.parent == self:
                    # parent of root is LootTree
                    drop_chances[' '.join(s for s in leaf.params)] = chance
                    break

                node = node.parent

        return drop_chances
            
# functional methods
def roll(macro_file):
    """
    Parse the macro, build the tree,
    and roll the results.
    Returns a list of rolled loot as
    keys.
    """
    tree = LootTree(macro_file)
    return tree.eval()


if __name__ == "__main__":
    tree = LootTree(open('../../example/adding_to_the_rolling_schema/macros/mob1.macro'))
    chances = tree.eval_dropchance()

    print "drop table:"
    for key in chances.keys():
        print key, "|", '{0:.2f}% chance'.format(chances[key] * 100.0)
    print "-----------------"

    print "drops:"
    loot = tree.eval()
    for item in loot:
        print item
    print "-----------------"