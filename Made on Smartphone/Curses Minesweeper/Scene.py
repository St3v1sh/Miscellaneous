from abc import ABC, abstractmethod

from Utility import Flow

class Scene(ABC):
	"""
	A scene of a game.
	Scenes can have different game logic, graphical logic, and controls.
	"""
	game = None  # A scene belongs to a Game.
	first_command = ""  # The hovered command when entering the Scene.
	
	@abstractmethod
	def parse(self, input):
		"""
		A scene must parse input and return an Action.
		
		input: the user input.
		return: an Action.
		"""
		pass
	
	@abstractmethod
	def act(self, action):
		"""
		A scene must respond to parsed input and return Flow.
		
		action: the Action to perform.
		return: a Flow.
		"""
		pass
	
	@abstractmethod
	def draw(self):
		"""A scene could have graphics."""
		pass
	
	def loop(self):
		"""The main loop of a scene."""
		while True:
			self.draw()
			
			action = self.parse(self.game.get_input())
			flow = self.act(action)
			
			if flow is Flow.RETURN:
				return
			elif flow is Flow.BREAK:
				break
			elif flow is Flow.CONTINUE:
				continue
			elif flow is Flow.PASS:
				pass
		
		self.game.stop()
