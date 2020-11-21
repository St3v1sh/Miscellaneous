import curses, curses.panel

class Graphics:
	"""
	A class for interfacing with curses functions. Graphics provides
	functions to manipulate the screen and a function to request user
	input.
	"""
	LENGTH = 60  # Length of screen in characters.
	HEIGHT = 30  # Height of screen in characters.
	
	STANDOUT = curses.A_STANDOUT  # Colors text to stand out.
	UNDERLINE = curses.A_UNDERLINE  # Underlines text.
	BOLD = curses.A_BOLD  # Bolds text.
	
	HIGHLIGHT = None  # Black text color and white background color.
	BRIGHT = None  # Brighter white text color.
	DIM = None  # Gray text color.
	DARK = None  # Black text color and black background color.
	MINE = None  # White text color and red background color.
	
	# Special characters
	ENTER_KEY = chr(10)  # Enter key.
	MINE_KEY = chr(0x00A4)  # Symbol used for mines.
	
	def __init__(self, screen):
		"""
		Constructs an instance of Graphics and returns it.
		
		screen: a standard screen object from the curses library.
		"""
		self.screen = screen  # Curses standard screen for graphics.
		
		# Initiate useful colors
		curses.init_pair(1, 16, 231)
		curses.init_pair(2, 231, 16)
		curses.init_pair(3, 240, 16)
		curses.init_pair(4, 16, 16)
		curses.init_pair(5, 231, 1)
		
		self.HIGHLIGHT = curses.color_pair(1)
		self.BRIGHT = curses.color_pair(2)
		self.DIM = curses.color_pair(3)
		self.DARK = curses.color_pair(4)
		self.MINE = curses.color_pair(5)
	
	def clear(self):
		"""Clears the screen."""
		for i in range(self.HEIGHT - 1):
			self.draw(0, i, " "*self.LENGTH, self.DARK)
		self.draw(0, self.HEIGHT - 1, " "*(self.LENGTH - 1), self.DARK)
		# Avoids a curses bug.
		params = (self.HEIGHT - 1, self.LENGTH - 1, " ", self.DARK)
		self.screen.insch(*params)
	
	def refresh(self):
		"""Refreshes the screen."""
		self.screen.refresh()
	
	def update_panels(self):
		"""Updates panels."""
		curses.panel.update_panels()
	
	def window_draw(self, window, x, y, input, color=0):
		"""
		Draws the input string on a window given x and y coordinates.
		
		window: the curses window to draw on.
		x: the x coordinate to start drawing input.
		y: the y coordinate to start drawing input.
		input: the string to draw.
		color: extra text decoration.
		"""
		# Make default color BRIGHT instead of system-defined
		color = color or self.BRIGHT
		window.addstr(y, x, input, color)
	
	def draw(self, x, y, input, color=0):
		"""
		Draws the input string on the global window given x and y
		coordinates.
		
		x: the x coordinate to start drawing input.
		y: the y coordinate to start drawing input.
		input: the string to draw.
		color: extra text decoration.
		"""
		self.window_draw(self.screen, x, y, input, color)
	
	def center_justify(self, y, input):
		"""
		Center justifies input at y position and returns a tuple
		(x, y, input).
		
		y: the desired y-position.
		input: the string to draw.
		return: a tuple with center-justified parameters.
		"""
		return ((self.LENGTH - len(input))//2, y, input)
	
	def right_justify(self, y, input):
		"""
		Right justifies input at y position and returns a tuple
		(x, y, input).
		
		y: the desired y-position.
		input: the string to draw.
		return: a tuple with right-justified parameters.
		"""
		return ((self.LENGTH - len(input)), y, input)
	
	def get_input(self):
		"""
		Gets a one-character input from the user between the ascii
		values 31 and 127 (exclusive) or the value 10 (enter key) and
		returns the character. If characters not in range are received,
		the function will keep querying.
		
		return: a character.
		"""
		while True:
			input = self.screen.getch()
			if 31 < input < 127 or input in [10]:
				return chr(input)
	
	def new_window(self, height, length, y, x):
		"""
		Creates a new curses window and returns it.
		
		height: the height of the window.
		length: the length of the window.
		y: the y-position of the window.
		x: the x-position of the window.
		return: a curses window with the given parameters.
		"""
		return curses.newwin(height, length, y, x)
	
	def new_panel(self, window):
		"""
		Creates a new curses panel and returns it.
		
		window: the window to use as a panel.
		return: a curses panel with the given window.
		"""
		return curses.panel.new_panel(window)
	
	def delete_panel(self, panel):
		"""
		Deletes a curses panel.
		
		panel: the curses panel to delete.
		"""
		del panel
