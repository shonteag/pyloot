"""
A demonstration of adding a currency item to
the rolling macros and tables.
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


class CurrencyItem(Item.BaseItem):
	"""
	Currency is a 'special' type of item, in that
	it has no stats, but has an amount.

	So the macro would look as such:

		drop currency_key ( min max )
		drop gold_coin ( 10 30 )

	to drop between 10 and 30 gold_coin.
	The lookup package will return the values
	10 and 30 in the BaseItem.args property.
	"""

	def roll_stats(self):
		"""
		So let's begin by overriding the stat rolling
		method, since there aren't any stats.

		Remember, this is called automatically by
		the Item.BaseItem's __init__ method.

		The min and max parameters will be in the
		BaseItem.keylist, since they are passed
		in by the macro roller.
		['currency', 'gold_coin']

		The amounts will have been parsed into the
		BaseItem.args property as a list.
		['10', '30']
		"""
		super(CurrencyItem, self).roll_stats()

		# start by getting the min and max
		minamount, maxamount = self.args[0], self.args[1]
		# remove min and max from the list

		self.amount = random.randint(int(minamount), int(maxamount))

	def get_amount(self):
		return self.amount

	def get_name(self):
		return str(self.statdict['name'])


if __name__ == "__main__":
	# SETTING UP THE LOOKUP
	# pipe down, parser.
	parser.suppress_warnings(True)

	# register tables
	Instance.register(parser.parse('tables/currency.table'))
	Instance.register(parser.parse('tables/key.table'))

	# register the base class
	Instance.register_item_class("currency", CurrencyItem)
	Instance.register_item_class("key", CurrencyItem)

	# ROLLING THE LOOT
	# build the decision tree from a mob's macro
	tree = Tree.LootTree(open('macros/moneymob.macro'))
	loot_keys = tree.eval()

	# use the generator in Instance to
	# iterate over returned list of loot keys.
	for item in Instance.items(loot_keys):
		print "{0}: {1} x{2}".format(item.get_type(), item.get_name(), item.get_amount())