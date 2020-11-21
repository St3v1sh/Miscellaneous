import os
import SceneManager as sm

from Scene import Scene
from Utility import Flow, Direction, Action
from UIElements import Button, Popup

class MenuScene(Scene):
	"""
	The menu scene provides controls to allow the player to navigate the
	main menu. In the main menu, the player can start a new game,
	continue an existing game, delete a saved game, and see controls.
	"""
	def __init__(self, game):
		"""
		Constructs an instance of MenuScene and returns it.
		
		game: the game class.
		"""
		# The game this scene belongs to.
		self.game = game
		
		# The first hovered command.
		self.first_command = "m"
		
		# The graphics class.
		self.graphics = game.graphics
		
		# The list of drawn Buttons.
		self.buttons = []
		
		# The index of the selected Button.
		self.select = None
		
		# True if there's a saved game.
		self.has_save = os.path.exists(self.game.SAVE_FILE)
		
		# Map of commands to functions.
		self.commands = {
			"q": self.quit,
			"w": lambda amt=1: self.move_cursor(Direction.UP, amt),
			"a": lambda amt=1: self.move_cursor(Direction.LEFT, amt),
			"s": lambda amt=1: self.move_cursor(Direction.DOWN, amt),
			"d": lambda amt=1: self.move_cursor(Direction.RIGHT, amt),
			"m": self.click
		}
		
		# Initialize Buttons.
		x, _, _ = self.graphics.center_justify(0, "Delete Save")
		
		color_options = (0, self.graphics.HIGHLIGHT, self.graphics.DIM)
		continue_b = Button(x, 13, "Continue", *color_options)
		new_game_b = Button(x, 14, "New Game", *color_options)
		del_save_b = Button(x, 15, "Delete Save", *color_options)
		
		continue_b.set_action(self.continue_game)
		new_game_b.set_action(self.new_game)
		del_save_b.set_action(self.delete_game)
		self.buttons = [continue_b, new_game_b, del_save_b]
		
		if not self.has_save:
			continue_b.set_enabled(False)
			del_save_b.set_enabled(False)
			self.select = 1
		else:
			self.select = 0
		
		self.buttons[self.select].set_hovered(True)
	
	def quit(self):
		"""Stops the game loop."""
		return Flow.BREAK
	
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
		
		bs = self.buttons
		indices = range(len(bs))
		enabled_b_i = [i for i in indices if bs[i].is_enabled()]
		current = enabled_b_i.index(self.select)
		next = enabled_b_i[(current + amount) % len(enabled_b_i)]
		
		bs[current].set_hovered(False)
		bs[next].set_hovered(True)
		self.select = next
		
		return Flow.PASS
	
	def click(self):
		"""Clicks the selected Button and returns a Flow."""
		return self.buttons[self.select].click()
	
	def continue_game(self):
		"""
		Provides functionality to the continue Button and returns a
		Flow.
		"""
		self.game.last_valid_command = "m"
		return Flow.PASS
	
	def new_game(self):
		"""
		Provides functionality to the new game Button and returns a
		Flow. Flow.RETURN is returned to reach NewGameScene. Flow.PASS
		is returned to remain on the MenuScene.
		"""
		self.game.last_valid_command = "m"
		if self.has_save:
			msg = (
				"You are about to override your save file with a new "
				"game. Do you want to proceed?"
			)
			popup = Popup(self, "OVERRIDE  SAVE", msg)
			if popup.query():
				self.game.change_scene(sm.mk_NewGameScene(self.game))
				return Flow.RETURN
		else:
			self.game.change_scene(sm.mk_NewGameScene(self.game))
			return Flow.RETURN
		return Flow.PASS
	
	def delete_game(self):
		"""
		Provides functionality to the delete game Button and returns a
		Flow.
		"""
		self.game.last_valid_command = "m"
		msg = (
			"You are about to delete your saved game. Do you want to "
			"proceed?"
		)
		popup = Popup(self, "DELETE  SAVE", msg)
		if popup.query():
			os.remove(self.game.SAVE_FILE)
			
			# Reconfigure Buttons.
			self.buttons[0].set_enabled(False)
			self.buttons[1].set_hovered(True)
			self.buttons[2].set_hovered(False)
			self.buttons[2].set_enabled(False)
			self.select = 1
			self.has_save = False
		return Flow.PASS
	
	def parse(self, input):
		"""
		Parses input and returns an Action.
		
		input: the user input.
		return: an Action.
		"""
		try:
			amt = int(input)
			return Action(self.game.last_valid_command, (amt,))
		except ValueError:
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
		"""Draws the main menu and selection options."""
		g = self.graphics
		g.clear()
		
		# Draw the MINESWEEPER banner.
		self.draw_title()
		
		# Draw the Buttons.		
		for button in self.buttons:
			buffer = button.to_tuple()
			for piece in buffer:
				g.draw(*piece)
		
		# Draw the info box.
		self.draw_info()
		
		# Draw controls.
		g.draw(0, g.HEIGHT-3, "_"*g.LENGTH)
		g.draw(1, g.HEIGHT-2, "wasd: Move | m: Select | q: Quit")
	
	def draw_title(self):
		"""Draws the MINESWEEPER banner."""
		g = self.graphics
		
		banner = [
			r"  __ __ _ __  _ ___  __  _   _ ___ ___ ___ ___ ___  ",
			r" |  V  | |  \| | __/' _/| | | | __| __| _,\ __| _ \ ",
			r" | \_/ | | | ' | _|`._`.| 'V' | _|| _|| v_/ _|| v / ",
			r" !_! !_!_!_!\__!___!___/!_/ \_!___!___!_! !___!_!_\ "
		]
		for i in range(len(banner)):
			g.draw(*g.center_justify(i+4, banner[i]))
	
	def draw_info(self):
		"""Draws some infomation about the hovered Button."""
		g = self.graphics
		
		message = ""
		if self.select == 0:
			message = "Continue a saved game."
		elif self.select == 1:
			message = "Start a new game."
		elif self.select == 2:
			message = "Delete the saved game."
		
		g.draw(0, 21, "_"*g.LENGTH)
		g.draw(1, 22, message)
