import textwrap

from abc import ABC, abstractmethod

class Popup:
	"""
	Creates a pop-up with "n" or "y" Buttons and returns True if y is
	clicked, False otherwise.
	"""
	def __init__(self, scene, title="", text=""):
		"""
		Constructs an instance of Graphics and returns it.
		
		scene: the Scene that this Popup belongs to.
		title: the title of the Popup.
		text: the text to display.
		"""
		# The Scene that this Popup belongs to.
		self.main_scene = scene
		
		# The title of the Popup.
		self.title = title
		
		# The text to display.
		self.text = text
		
		# The game object.
		self.game = scene.game
		
		# The graphics class.
		self.graphics = self.game.graphics
		
		# The list of drawn Buttons.
		self.buttons = []
		
		# The index of the selected Button.
		self.select = 0
		
		# Drawing values
		self.length = 60
		self.height = 10
		self.x = 0
		self.y = 10
		self.text_length = 40
		self.text_height = 6
		
		# Initialize Buttons.
		color_options = (0, self.graphics.HIGHLIGHT)
		no_b = Button(24, self.height - 2, "N", *color_options)
		
		position = (self.length - 25, self.height - 2)
		yes_b = Button(*position, "Y", *color_options)
		self.buttons = [no_b, yes_b]
		self.selected = 0
		no_b.set_hovered(True)
		
		# Initialize panel.
		panel_options = (self.height, self.length, self.y, self.x)
		self.window = self.graphics.new_window(*panel_options)
		self.panel = self.graphics.new_panel(self.window)
	
	def delete_popup(self):
		"""Deletes the Popup panel."""
		self.graphics.delete_panel(self.panel)
		self.graphics.update_panels()
		self.graphics.refresh()
	
	def draw(self, x, y, input, color=0):
		"""Draws on the Popup panel."""
		g = self.graphics
		g.window_draw(self.window, x, y, input, color)
	
	def query(self):
		"""
		Asks the user a Y/N question and returns a boolean.
		
		return: True if Y is picked, False otherwise.
		"""
		g = self.graphics
		
		# Draw decorations.
		self.draw_decorations()
		
		# Loop for user input.
		while True:
			# Draw Buttons.
			for button in self.buttons:
				buffer = button.to_tuple()
				for piece in buffer:
					self.draw(*piece)
			g.update_panels()
			g.refresh()
			
			# Check input.
			inp = g.get_input()
			if inp == "q":
				self.delete_popup()
				return False
			elif inp in ["w", "a", "s", "d", g.ENTER_KEY]:
				self.buttons[self.selected].set_hovered(False)
				self.selected = (self.selected + 1) % 2
				self.buttons[self.selected].set_hovered(True)
			elif inp == "m":
				self.delete_popup()
				return self.selected
			elif inp == "y":
				self.delete_popup()
				return True
	
	def draw_decorations(self):
		"""Draws Popup decorations."""
		g = self.graphics
		
		# Drawing values
		length = self.length
		height = self.height
		x = self.x
		y = self.y
		text_length = self.text_length
		text_height = self.text_height
		
		# Draw decorations.
		self.draw(0, 0, "="*length, g.BRIGHT)
		self.draw(0, height - 1, "="*(length - 1), g.BRIGHT)
		# Avoids a curses bug.
		self.window.insch(height - 1, length - 1, "=", g.BRIGHT)
		color_op = g.BRIGHT | g.UNDERLINE
		self.draw(9, 1, " "*(text_length + 2), color_op)
		self.draw(9, text_height + 1, "_"*(text_length + 2), g.BRIGHT)
		
		self.draw(4, 1,  "_", g.DIM)
		self.draw(3, 2, "| |", g.DIM)
		self.draw(3, 3, "| |", g.DIM)
		self.draw(3, 4, "| |", g.DIM)
		self.draw(3, 5, "!_!", g.DIM)
		self.draw(4, 6,  "_", g.DIM)
		self.draw(3, 7, "!_!", g.DIM)
		
		self.draw(length - 5, 1,  "_", g.DIM)
		self.draw(length - 6, 2, "| |", g.DIM)
		self.draw(length - 6, 3, "| |", g.DIM)
		self.draw(length - 6, 4, "| |", g.DIM)
		self.draw(length - 6, 5, "!_!", g.DIM)
		self.draw(length - 5, 6,  "_", g.DIM)
		self.draw(length - 6, 7, "!_!", g.DIM)
		
		# Draw title.
		x_val = (length - len(self.title))//2
		color_op = g.BRIGHT | g.UNDERLINE| g.BOLD
		self.draw(x_val, 1, self.title, color_op)
		
		# Draw text.
		tl = text_length
		th = text_height
		wrapper = textwrap.TextWrapper(width=tl, max_lines=th)
		lines = wrapper.wrap(text=self.text)
		for i, line in enumerate(lines, 0):
			self.draw(10, i + 2, line, g.BRIGHT)

class UIElement(ABC):
	"""UI elements provide easier ways for IO using curses"""
	@abstractmethod
	def to_tuple(self):
		"""
		A UIElement must have a tuple representation.
		
		return: a list of tuples of the form (x, y, text, color).
		"""
		pass

class NumberField(UIElement):
	"""
	A NumberField provides a structure to store the information required
	to interact with a text-based number field. It also provides a
	mechanism for a user to input a number.
	"""
	def __init__(self, x, y, value=0, min=0, max=100, prefix="",
				 postfix="", color=0, hover_color=0, edit_color=0,
				 disabled_color=0, enabled=True):
		"""
		Constructs an instance of NumberField and returns it.
		
		x: the x-position of the NumberField.
		y: the y-position of the NumberField.
		value: the default display value.
		min: the minimum value.
		max: the maximum value.
		prefix: a prefix to add to the value.
		postfix: a postfix to add to the value.
		color: the default color of the NumberField.
		hover_color: the color of the NumberField when hovered.
		disabled_color: the color of the NumberField when disabled.
		enabled: an enabled Button can be hovered and clicked.
		"""
		pass

class Button(UIElement):
	"""
	A Button provides a structure to store the information required to
	interact with a text-based button.
	"""
	def __init__(self, x, y, text, color=0, hover_color=0,
				 disabled_color=0, enabled=True, action=lambda: None):
		"""
		Constructs an instance of Button and returns it.
		
		x: the x-position of the Button.
		y: the y-position of the Button.
		text: the text on the Button.
		color: the default color of the Button.
		hover_color: the color of the Button when hovered.
		disabled_color: the color of the Button when disabled.
		enabled: an enabled Button can be hovered and clicked.
		action: the function to execute when the Button is clicked.
		"""
		self.x = x
		self.y = y
		self.text = text
		self.color = color
		self.hover_color = hover_color
		self.disabled_color = disabled_color
		self.enabled = enabled
		self.hovered = False
		self.action = action
	
	def set_color(self, color):
		"""
		Sets the idle color of the Button.
		
		color: the new color.
		"""
		self.color = color
	
	def set_hover_color(self, color):
		"""
		Sets the hovered color of the Button.
		
		color: the new hovered color.
		"""
		self.hover_color = color
	
	def set_disabled_color(self, color):
		"""
		Sets the disabled color of the Button.
		
		color: the new disabled color.
		"""
		self.disabled_color = color
	
	def set_enabled(self, enabled):
		"""
		Changes the Button's enabled value. A disabled Button uses
		inactive_color.
		
		enabled: the new enabled value.
		"""
		self.enabled = enabled
	
	def is_enabled(self):
		"""Returns True if the Button is enabled. False otherwise."""
		return self.enabled
	
	def set_hovered(self, hovered):
		"""
		Changes the Button's hovered value. A hovered Button uses
		hover_color.
		
		hovered: the new hovered value.
		"""
		if self.is_enabled():
			self.hovered = hovered
	
	def is_hovered(self):
		"""
		Returns True if the button is hovered and enabled. False
		otherwise.
		"""
		return self.hovered and self.is_enabled
	
	def set_action(self, action):
		"""
		Changes the Button's action function.
		
		action: the new function to run when the Button is clicked.
		"""
		self.action = action
	
	def click(self, params=()):
		"""
		Executes the action function given to the Button and retuns the
		result. The Button needn't be hovered nor active.
		
		params: function parameters to be passed onto action().
		"""
		return self.action(*params)
	
	def to_tuple(self):
		"""
		Generates a tuple (x, y, text, color) to represent the current
		state of the Button and returns it.
		"""
		color = self.color
		if self.is_hovered():
			color = self.hover_color
		elif not self.is_enabled():
			color = self.disabled_color
		return [(self.x, self.y, self.text, color)]
