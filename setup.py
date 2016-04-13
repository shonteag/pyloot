#/usr/bin/python

from distutils.core import setup

# third-party modules
with open('requirements.txt') as f:
	requirements = f.read().splitlines()

setup(
	name = "pyloot",
	version = "1.0",
	description = "RPG-style loot rolling in Python",
	author = "Shonte Amato-Grill",
	url = "https://github.com/shonteag/pyloot",
	license = "MIT",
	package_dir = {"pyloot": "src"},
	packages = ["pyloot", "pyloot.roller", "pyloot.lookup"],
	install_requires = requirements
	)