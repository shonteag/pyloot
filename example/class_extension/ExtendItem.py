import sys
import os
path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))
sys.path.append(os.path.abspath(path))
from src.roller import Tree
from src.lookup import Instance, parser, Item


class ExtendedBaseItem(Item.BaseItem):
	"""the base class for all items in our game"""
	def __init__(self, *args, **kwargs):
		super(ExtendedBaseItem, self).__init__(*args, **kwargs)
		
	def get_type(self):
		# primary key in the lookup table
		# weapon, armor, etc
		return self.keylist[0]

	def get_name(self):
		return str(self.statdict['name'])


class WeaponItem(ExtendedBaseItem):
	"""the subclass for all weapons in our game"""
	def __init__(self, *args, **kwargs):
		super(WeaponItem, self).__init__(*args, **kwargs)
	
	def get_type(self):
		return "weapon"

class BowItem(WeaponItem):
	"""the subclass for all bow weapons in our game"""
	def __init__(self, *args, **kwargs):
		super(BowItem, self).__init__(*args, **kwargs)

	def get_type(self):
		return "weapon-ranged"

class SwordItem(WeaponItem):
	"""the sublcass for all sword weapons in our game"""
	def __init__(self, *args, **kwargs):
		super(SwordItem, self).__init__(*args, **kwargs)

	def get_type(self):
		return "weapon-sword"


class ArmorItem(ExtendedBaseItem):
	"""the subclass for all armor in our game"""
	def __init__(self, *args, **kwargs):
		super(ArmorItem, self).__init__(*args, **kwargs)

	def get_type(self):
		return "armor"


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

	# register item subclasses
	Instance.register_item_class("weapon", WeaponItem)
	Instance.register_item_class("armor", ArmorItem)
	# chaining two subkeys together to get a more
	# specific item class! All items in category
	# "weapon", and subcategory "bow" will be of type
	# BowItem.
	Instance.register_item_class("weapon:bow", BowItem)
	# can also use the Item.list_to_dict_key() method
	Instance.register_item_class(
		Item.list_to_dict_key(['weapon', 'sword']),
		SwordItem)

	# ROLLING THE LOOT
	# build the decision tree from a mob's macro
	tree = Tree.LootTree(open('macros/mob1.macro'))
	loot_keys = tree.eval()

	# use the generator in Instance to
	# iterate over returned list of loot keys.
	for item in Instance.items(loot_keys):
		print item.get_name(), ",", item.get_type(), ",", item.__class__