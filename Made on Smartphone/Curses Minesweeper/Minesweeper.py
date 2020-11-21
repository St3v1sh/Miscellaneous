"""
This project uses curses and curses.panel. curses isn't supported on
Windows machines, but you may use `pip install windows-curses`. However,
I don't know of a way to use curses.panel on Windows. Also, this program
requires a 256-colored terminal.

This program was written on my smartphone.
This is the first serious project I started on my phone. Currently, it's
still in development. I'm using curses instead of printing a buffer to
the output.
"""
import curses
import SceneManager as sm

from Graphics import Graphics

class Game:
	"""A class for starting a game of Minesweeper."""
	SAVES_PATH = "./Saves/"
	SAVE_FILE = SAVES_PATH + "minefield.save"
	
	def __init__(self, screen):
		"""
		Constructs an instance of Game and returns it.
		
		screen: a standard screen object from the curses library.
		"""
		# Create a Graphics class to handle drawing.
		self.graphics = Graphics(screen)
		
		# The last valid input by the user.
		self.last_valid_command = ""
		
		# Controls the game loop.
		self.running = True
		
		# Current scene.
		self.scene = None
	
	def start(self):
		"""Starts the game loop at the menu scene."""
		self.change_scene(sm.mk_MenuScene(self))
		self.loop()
	
	def loop(self):
		"""Main game loop."""
		while self.running:
			self.scene.loop()
	
	def change_scene(self, scene, command=""):
		"""Sets the next scene."""
		self.scene = scene
		if command == "":
			command = scene.first_command
		self.last_valid_command = command
	
	def stop(self):
		"""Stops the game loop."""
		self.running = False
	
	def get_input(self, message="", show_default=True, repeat=chr(10)):
		"""
		Gets a one-character input from the user and returns it. A
		message and a default response are also drawn to the screen.The
		default response is returned if the user inputs the enter key.
		
		message: a string displayed before requesting user input.
		show_default: shows the default response if True.
		return: a character input.
		"""
		x = 0
		y = self.graphics.HEIGHT-1
		if show_default:
			input = "{} ({})".format(message, self.last_valid_command)
		else:
			input = message
		self.graphics.draw(x, y, input)
		
		key = self.graphics.get_input()
		if key == repeat:
			return self.last_valid_command
		return key

def main(screen):
	"""The function to be used by the curses wrapper."""
	curses.curs_set(False)  # Disables cursor.
	
	# Create a Game instance and start the game.
	game = Game(screen)
	game.start()
	
if __name__ == "__main__":
	curses.wrapper(main)
