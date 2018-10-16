__version__ = '0.2.6'

import yaml
import os
import logging

from addict import Dict as _Dict
from pprint import pformat

__all__ = ('yaml', 'Dict')

def _prettyprint_fallback(x):
	if isinstance(x, _Dict):
		return repr(x)
	else:
		return pformat(x)

class Dict(_Dict):

	def __repr__(self):
		if self.keys():
			m = max(map(len, list(str(_) for _ in self.keys()))) + 1
			return '\n'.join(['┣'+str(k).rjust(m) + ': ' + _prettyprint_fallback(v).replace('\n','\n┃'+' '*(m+2)) for k, v in self.items()])
		else:
			return self.__class__.__name__ + "()"

	@classmethod
	def load(cls, filename, *args, logger=None, **kwargs):
		"""

		Parameters
		----------
		filename : str
			A filename of a yaml file to load, or a yaml file contents as a string.  
		args
		allow_json
		kwargs

		Returns
		-------
		Dict
		"""
		from .yaml_checker import yaml_check
		if isinstance(filename, str) and '\n' not in filename:
			if not os.path.exists(filename):
				raise FileNotFoundError(filename)
			try:
				yaml_check(filename, logger=logging.getLogger('') if logger is None else logger)
				with open(filename, 'r') as f:
					return cls(yaml.load(f, *(args[1:]), **kwargs))
			except Exception as err:
				print("~"*40)
				print(f"ERROR READING {filename}")
				print("~"*40)
				raise

		else:
			return cls(yaml.load(filename, *args, **kwargs))

	@classmethod
	def load_multi(cls, *filenames, **kwargs):
		"""

		Parameters
		----------
		filenames : tuple of str
		kwargs

		Returns
		-------
		Dict
		"""
		filename = filenames[0]
		x = cls.load(filename, **kwargs)
		for filename in filenames[1:]:
			y = cls.load(filename, **kwargs)
			x.update(y)
		return x

	def dump(self, *args, **kwargs):
		from yaml import dump
		if 'default_flow_style' not in kwargs:
			kwargs['default_flow_style'] = False
		if 'indent' not in kwargs:
			kwargs['indent'] = 2
		if len(args) and isinstance(args[0], str):
			if os.path.exists(args[0]):
				raise FileExistsError(args[0])
			dirname = os.path.dirname(args[0])
			if not os.path.exists(dirname):
				os.makedirs(dirname)
			with open(args[0], 'w') as f:
				dump(self.to_dict(), f, *(args[1:]), **kwargs)
		else:
			return dump(self.to_dict(), *args, **kwargs)
