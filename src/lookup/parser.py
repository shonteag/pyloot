"""
A table parsing utility module.
Can handle json and xml files.

from lookup import parser
loaded_dict = parser.parse("path/to/file")
"""
import sys
import json
import xmltodict
import warnings


SUPPRESS_WARNINGS = False

# parsing methods
def parse_xml(file_path):
	return xmltodict.parse(open(file_path).read())

def parse_json(file_path):
	return json.load(open(file_path))

# registered parsers and handlers
PARSERS = {
	'xml': parse_xml,
	'json': parse_json
}

def register_parser(parser_key, parser_method):
	"""
	Allows the caller to create their own
	parsing methods.
	Custom parsing methods *must* accept
	the file_path as the only argument,
	an return a dict.
	"""
	PARSERS.update({parser_key, parser_method})

def suppress_warnings(flag):
	"""
	Used to tell the module to shut the
	hell up about not finding the right
	parser on the first try.
	"""
	setattr(sys.modules[__name__], "SUPPRESS_WARNINGS", bool(flag))

def parse(file_path, parser_key=None):
	"""
	Tries all available parsers until
	one works.
	Warns user if wrong type, to avoid
	silent error catching.
	Throws FormatError if no parser
	is found for the file.
	"""
	if parser_key in PARSERS:
		# if the user specifies a parser
		return PARSERS[parser_key](file_path)

	# if no specific parser, try to match
	for parser in PARSERS:
		try:
			return PARSERS[parser](file_path)
		except:
			if not SUPPRESS_WARNINGS:
				warnings.warn("parser of incorrect type ({0}),"\
					" proceeding to next type".format(parser))

	# gets called if no parser is a match.
	raise FormatError("unable to parse '{0}'".format(file_path))
	return {}