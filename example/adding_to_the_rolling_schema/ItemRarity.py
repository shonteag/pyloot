"""
This implements a rarity system, pretty standard
to most RPG loot systems.  Every item has a range
in 1 to 100, and the ExtendedBaseItem (which overrides
the base Item) uses a preconfigured range to determine
Common, Magical, Epic, Artifact.
"""

import sys
import os
path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))
sys.path.append(os.path.abspath(path))
from src.roller import Tree
from src.lookup import Instance, parser, Item

import random


RARITY_SCORE = [
	30, 67, 95, 100
]
RARITY = [
	"Common", "Magical", "Epic", "Artifact"
]


class ExtendedBaseItem(Item.BaseItem):
	"""the base class for all items in our game"""
	def __init__(self, *args, **kwargs):
		super(ExtendedBaseItem, self).__init__(*args, **kwargs)

	def get_name(self):
		return str(self.statdict['name'])

	def get_type(self):
		# primary key in the lookup table
		# weapon, armor, etc
		return self.keylist[0]

	def get_rarity(self):
		return RARITY[self.get_rarity_()]
	def get_rarity_(self):
		# raw number
		return self.statdict["rarity"]

	# override
	def roll_stats(self):
		# roll all the base stats
		super(ExtendedBaseItem, self).roll_stats()

		# determine rarity
		if "rarity" not in self.statdict:
			self.statdict["rarity"] = random.randint(1, 100)

		val = self.statdict["rarity"]

		for rarity, maxval in zip(enumerate(RARITY), RARITY_SCORE):
			if val <= maxval:
				self.statdict["rarity"] = rarity[0]
				break

if __name__ == "__main__":
	# SETTING UP THE LOOKUP
	# pipe down, parser.
	parser.suppress_warnings(True)

	# register tables
	Instance.register(parser.parse('tables/weapon.table'))
	Instance.register(parser.parse('tables/namedweapon.table'))
	Instance.register(parser.parse('tables/armor.xml'))

	# register item base class
	Instance.set_item_class(ExtendedBaseItem)

	# ROLLING THE LOOT
	# build the decision tree from a mob's macro
	tree = Tree.LootTree(open('macros/mob1.macro'))
	loot_keys = tree.eval()

	# use the generator in Instance to
	# iterate over returned list of loot keys.
	for item in Instance.items(loot_keys):
		print "{0}: {1} ({2})".format(item.get_type(), item.get_name(), item.get_rarity())
