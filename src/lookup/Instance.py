import random
import Item
import Error

TABLE = {}

def _merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

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
		table = table[keylist[i]]
	return Item.Item(table)

def items(list_of_keylists):
	for keylist in list_of_keylists:
		yield lookup(keylist)
