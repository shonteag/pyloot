import random
import Error


class BaseItem(object):
	"""
	An extendable class for housing the
	Item object, which knows how to roll
	it's own stats as detailed in the
	table file.
	"""

	def __init__(self, initdict, keylist):
		"""
		Initializer takes the a dictionary
		extracted from the *.table files by
		the Instance module.
		"""
		self.keylist = keylist
		self.itemdict = initdict
		self.statdict = {}
		self.set_stats()

	def set_stats(self):
		"""
		Rolls stats onto the item, as detailed
		in the items archetype in the *.table
		file from which it originates.
		"""
		for key in self.itemdict.keys():
			value = self.itemdict[key]
			value_ = value.split(" ")
			if len(value_) > 1 and value_[0] == "roll":
				params = value_[1:]
				value = random.randint(int(params[0]), int(params[1]))

			if key in self.statdict:
				raise Error.KeyConflictError(
					"key conflict {0} already in loot table".format(
						key))

			self.statdict[key] = value

	def __str__(self):
		"""to string"""
		string = ""
		for key in self.statdict:
			string += "{0}: {1}, ".format(key, self.statdict[key])
		return string