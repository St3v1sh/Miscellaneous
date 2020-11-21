import os
import math
import SceneManager as sm

from Scene import Scene
from Utility import Flow, Direction, Action
from UIElements import Button

class NewGameScene(Scene):
	"""
	The new game scene provides buttons and number fields for definining
	the game parameters for a new minesweeper game.
	"""
	def __init__(self, game):
		"""
		Constructs an instance of NewGameScene and returns it.
		
		game: the game class.
		"""
		# The game this scene belongs to.
		self.game = game
		
		# The first hovered command.
		self.first_command = "d"
		
		# The graphics class.
		self.graphics = game.graphics
		
		# The list of drawn Buttons.
		self.buttons = []
		
		# The index of the selected Button.
		self.select = 0
		
		# True if there's a saved game.
		self.has_save = os.path.exists(self.game.SAVE_FILE)
		
		# Map of commands to functions.
		self.commands = {
			"q": self.quit,
			"w": lambda amt=1: self.move_cursor(Direction.UP, amt),
			"a": lambda amt=1: self.move_cursor(Direction.LEFT, amt),
			"s": lambda amt=1: self.move_cursor(Direction.DOWN, amt),
			"d": lambda amt=1: self.move_cursor(Direction.RIGHT, amt)
		}
		
		# Minefield options
		self.options = {
			"easy": {
				"length": 10,
				"height": 10,
				"density": 10
			},
			"medium": {
				"length": 30,
				"height": 20,
				"density": 15
			},
			"hard": {
				"length": 60,
				"height": 30,
				"density": 20
			},
			"custom": {
				"length": 10,
				"height": 10,
				"density": 10
			}
		}
		
		# Initialize Buttons.
		color_options = (0, self.graphics.HIGHLIGHT)
		easy = Button(1, 4, "Easy", *color_options)
		medium = Button(1, 5, "Medium", *color_options)
		hard = Button(1, 6, "Hard", *color_options)
		custom = Button(1, 7, "Custom", *color_options)
		
		self.buttons = [easy, medium, hard, custom]
		self.buttons[self.select].set_hovered(True)
	
	def quit(self):
		"""Returns to the main menu and returns Flow.RETURN."""
		self.game.change_scene(sm.mk_MenuScene(self.game))
		return Flow.RETURN
	
	def move_cursor(self, dir, amount):
		"""
		Takes a direction and move amount and moves the cursor. Returns
		a Flow.
		
		dir: the Direction to move.
		amount: the amount to move in the given Direction.
		return: a Flow.
		"""
		if dir is Direction.UP:
			amount *= -1
			self.game.last_valid_command = "w"
		elif dir is Direction.LEFT:
			amount *= -1
			self.game.last_valid_command = "a"
		elif dir is Direction.DOWN:
			self.game.last_valid_command = "s"
		elif dir is Direction.RIGHT:
			self.game.last_valid_command = "d"
		
		next = (self.select + amount) % len(self.buttons)
		self.buttons[self.select].set_hovered(False)
		self.buttons[next].set_hovered(True)
		self.select = next
		
		return Flow.PASS
	
	def parse(self, input):
		"""
		Parses input and returns an Action.
		
		input: the user input.
		return: an Action.
		"""
		return Action(input)
	
	def act(self, action):
		"""
		Responds to parsed input with side effects and returns Flow.
		
		action: the Action to perform.
		return: a Flow.
		"""
		command = self.commands.get(action.primary, None)
		if command is not None:
			try:
				return command(*action.secondary)
			except TypeError:
				return Flow.PASS
		return Flow.PASS
	
	def draw(self):
		"""Draws tools for starting a new game."""
		g = self.graphics
		g.clear()
		
		# Draw title.
		msg = "CHOOSE  DIFFICULTY"
		centered = g.center_justify(1, msg)
		g.draw(*centered, g.BOLD)
		g.draw(0, 2, "_"*g.LENGTH)
		
		# Draw the Buttons.
		for button in self.buttons:
			buffer = button.to_tuple()
			for piece in buffer:
				g.draw(*piece)		
		g.draw(0, 8, "_"*g.LENGTH)
		
		# Draw the info box.
		self.draw_info()
		
		# Draw controls.
		g.draw(0, g.HEIGHT-3, "_"*g.LENGTH)
		g.draw(1, g.HEIGHT-2, "wasd: Move | m: Select | q: Quit")
	
	def draw_info(self):
		"""Draws some infomation about the hovered Button."""
		g = self.graphics
		
		message = ""
		length = 10
		height = 10
		density = 10
		if self.select == 0:
			message = "Small field and easy mine density."
			length = self.options["easy"]["length"]
			height = self.options["easy"]["height"]
			density = self.options["easy"]["density"]
		elif self.select == 1:
			message = "Increased field area and mine density."
			length = self.options["medium"]["length"]
			height = self.options["medium"]["height"]
			density = self.options["medium"]["density"]
		elif self.select == 2:
			message = "Challenging field and mine density."
			length = self.options["hard"]["length"]
			height = self.options["hard"]["height"]
			density = self.options["hard"]["density"]
		elif self.select == 3:
			message = "Customized settings."
			length = self.options["custom"]["length"]
			height = self.options["custom"]["height"]
			density = self.options["custom"]["density"]

		g.draw(1, 10, message)
		
		g.draw(1, 12, "Difficulty statistics:")
		g.draw(1, 13, "Length: " + str(length))
		g.draw(1, 14, "Height: " + str(height))
		mines = math.floor(length * height * density / 100)
		mines_msg = "Mine density: {}% ({} mines)".format(density, mines)
		g.draw(1, 15, mines_msg)
		