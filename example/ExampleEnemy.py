"""
ExampleEnemy.py

This is an example of how to use PyLoot
in a game.

NOTE: This example DOES NOT include item
lookup tables. It ONLY rolls drop keys!
"""

# first we dupe python to import the package.
# this may not be necessary, depending on how
# you, as the developer, choose to use it.
import sys
import os
import json
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(path))
from src.roller.Tree import LootTree
from src.lookup import Instance

class ExampleEnemy(object):
	def __init__(self, name, macropath):
		self.name = name
		self.macropath = macropath

	def on_death(self):
		print "{0} has been killed!".format(self.name)
		tree = LootTree(open(self.macropath))
		loot_keys = tree.eval()

		for item in Instance.items(loot_keys):
			# you may also look into the lookup table
			# aspect of the package to match these
			# loot keys to actual items... and roll
			# stats onto them!
			print str(item)

			# at this point, you could use your own
			# methods to manipulate gear stats, such
			# as a weapons level, for instance.


if __name__ == "__main__":
	# setup the lookup, register the tables
	Instance.register(json.load(open('weapon.table')))
	Instance.register(json.load(open('namedweapon.table')))
	Instance.register(json.load(open('armor.table')))

	enemy = ExampleEnemy("Shonte", "mob1.macro")
	enemy.on_death()
