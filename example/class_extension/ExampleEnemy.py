"""
ExampleEnemy.py

This is an example of how to use PyLoot
in a game.  It shows, specifically, how
to override base classes in pyloot to
create customized functionality.

NOTE: This example DOES NOT include item
lookup tables. It ONLY rolls drop keys!
"""

import sys
import os
import json

# we dupe python to import the package.
# this is only necessary because pyloot
# is not on our python path.
path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))
sys.path.append(os.path.abspath(path))
from src.roller.Tree import LootTree
from src.lookup import Instance, parser, Item


class ExampleItem(Item.BaseItem):
    """
    override the BaseItem class in the 
    lookup subpackage
    """
    def __init__(self, *args, **kwargs):
        super(ExampleItem, self).__init__(*args, **kwargs)

    def get_name(self):
        return self.statdict['name']

    def get_types(self):
        return self.keylist

class ExampleEnemy(object):
    def __init__(self, name, macropath):
        self.name = name
        self.macropath = macropath

    def on_death(self):
        print "{0} has been killed!".format(self.name)

        # creating the loot tree from
        # the macro file for this example enemy.
        tree = LootTree(open(self.macropath))
        loot_keys = tree.eval()

        for item in Instance.items(loot_keys):
            # Instance.items() is a generator
            # which queries all loot_keys against
            # the pre-registered lookup tables.
            # The items it returns are of type
            # ExampleItem, because we told the
            # Instance module to use this class
            # in the initial setup.
            print item.get_name()
            print item.get_types()



if __name__ == "__main__":
    # First, let's tell the parser to be
    # quiet about not always finding the right
    # parser on the first try.
    parser.suppress_warnings(True)
    # setup the lookup, register the tables
    # We are using the pyloot package's
    # custom parser, which can handle both
    # xml and json files to table definitions.
    # A json file:
    Instance.register(parser.parse('tables/weapon.table'))
    # Another json file, which merges to the "weapon" key:
    Instance.register(parser.parse('tables/namedweapon.table'))
    # An XML file
    Instance.register(parser.parse('tables/armor.table'))

    # set the item class to override lookup.Item.BaseItem
    Instance.set_item_class(ExampleItem)

    enemy = ExampleEnemy("Shonte", "mob1.macro")  # create the enemy
    enemy.on_death()  # kill the enemy
