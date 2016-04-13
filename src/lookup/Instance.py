"""
The lookup subpackage's main module.
Used to register lookup table (dict),
and can be 'queried' to retrieve Items,
(which know how to roll their own stats).
"""
import sys
import random

import Item


TABLE = {}
ITEMCLASS = Item.BaseItem
ITEMSUBCLASS = {}

WILDCARD = "*"

def _merge(a, b, path=None):
    """
    merges b into a
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise KeyError(
                	'Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def set_item_class(item_class):
	"""
	Can be used to set the returned
	item object class (from lookups).
	Should be used if the user extends
	the Item.BaseItem class!
	"""
	setattr(sys.modules[__name__], "ITEMCLASS", item_class)

def register_item_class(key, item_class):
	"""
	Register a specific subclass to a
	key string, item.get_dict_key()
	"""
	ITEMSUBCLASS.update({str(key):item_class})

def register(table, append=True):
	"""
	register all primary keys in
	the new table to the Instance.tables
	"""
	TABLE.update(_merge(TABLE, table))

def lookup(keylist):
	"""
	key is of type list
	"""
	table = TABLE[str(keylist[0])]
	for i in range(1, len(keylist)):
		if keylist[i] == WILDCARD:
			# allow for wildcard rolling
			randomkey = random.choice(table.keys())
			table = table[randomkey]
			keylist[i] = randomkey
		else:
			table = table[keylist[i]]

	# find proper item sublcass
	lastfound = ITEMCLASS
	for j in range(1, len(keylist)):
		keylist_ = keylist[0:j]
		if Item.list_to_dict_key(keylist_) in ITEMSUBCLASS:
			lastfound = ITEMSUBCLASS[Item.list_to_dict_key(keylist_)]

	# if no special class, use base class
	return lastfound(table, keylist)

def items(list_of_keylists):
	"""
	generator for iterating over
	all 'dropped' keys from the
	roller subpackage.
	"""
	for keylist in list_of_keylists:
		yield lookup(keylist)
