from enum import Enum

class Flow(Enum):
	"""An enum used to provide flow control."""
	PASS = 0
	BREAK = 1
	CONTINUE = 2
	RETURN = 3

class Direction(Enum):
	"""An enum used to represent 2D directions."""
	UP = 0
	LEFT = 1
	DOWN = 2
	RIGHT = 3

class Action:
	"""
	An Action stores parsed information about what action(s) should be
	performed.
	"""
	def __init__(self, primary, secondary=()):
		"""
		Constructs an instance of Action and returns it.
		
		primary: the primary action.
		secondary: parameters for the primary action.
		"""
		self.primary = primary
		self.secondary = secondary
		self.action = (primary, secondary)
