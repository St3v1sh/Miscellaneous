"""
This program was written on my smartphone.
Now, I wanted to play with printing colored characters. This
implementation of Minesweeper is extremely messy, but it served its
purpose (to make me more used to using this IDE.)
"""
import random
from enum import Enum
from copy import deepcopy

class Graphics:
	def __init__(self):
		self.w = 60
		self.h = 29
		self.mt = "\x1b[90m.\x1b[00m"
		self.default_buffer = [[self.mt for _ in range(self.w)] for _ in range(self.h)]
		self.buffer = deepcopy(self.default_buffer)
		
	def print_buffer(self):
		for line in self.buffer:
			print("".join(line))
	
	def reset_buffer(self):
		self.buffer = deepcopy(self.default_buffer)
		
	def draw(self, obj, x, y):
		h = len(obj)
		for dy in range(h):
			w = len(obj[dy])
			self.buffer[y + dy][x:x+w] = obj[dy]
	
	def right_justify(self, obj, y):
		m = len(obj[0])
		for line in obj:
			if len(line) > m:
				m = len(line)
		return (obj, self.w-m, y)
	
	def to_obj(self, s):
		return [list(s)]
	
	def arr_to_obj(self, arr):
		return [list(s) for s in arr]

class Game:
	class Action(Enum):
		_NO_ACTION = 0
		_MOVE_ACTION = 1
		_DEFUSE_ACTION = 2
		_FLAG_ACTION = 3
		_CHEAT_ACTION = 4
		_FORCE_QUIT = 5
	
	class Flow(Enum):
		_NORMAL = 0
		_BREAK = 1
		_CONTINUE = 2
	
	def __init__(self):
		self.graphics = Graphics()
		self.w = self.graphics.w
		self.h = self.graphics.h
		self.mines = int((self.w*self.h*0.2))
		self.v_mines = self.mines
		self.flags = []
		self.field = None
		self.selected = None
		
		self.fla = "\x1b[31m!\x1b[00m"
		self.min = "\x1b[31m*\x1b[00m"
		self.sel = "\x1b[46m"
		self.res = "\x1b[00m"
	
	def safe_sweep(self, x, y, manual = False):
		v = self.graphics.buffer[y][x]
		if not (v == self.graphics.mt or v == self.sel+self.graphics.mt+self.res):
			return
		
		b = self.num(x, y)
		
		if b > 0:
			tmp = self.sel+str(b)+self.res if manual else str(b)
			obj = [[tmp]]
			self.graphics.draw(obj, x, y)
		else:
			tmp = self.sel+" "+self.res if manual else " "
			obj = [[tmp]]
			self.graphics.draw(obj, x, y)
			
			for i in range(max(y-1, 0), min(y+2, self.h)):
				for j in range(max(x-1, 0), min(x+2, self.w)):
					self.safe_sweep(j, i)
	
	def num(self, x, y):
		b = 0
		
		for i in range(max(y-1, 0), min(y+2, self.h)):
			for j in range(max(x-1, 0), min(x+2, self.w)):
				if self.field[i][j]:
					b += 1
		return b
	
	def select(self, x, y):
		if not self.selected is None:
			x_ = self.selected[0]
			y_ = self.selected[1]
			
			# Work-around: list() can't handle escape characters
			old = self.graphics.buffer[y_][x_][5:-5]
			obj = [[old]]
			self.graphics.draw(obj, x_, y_)
		
		v = self.graphics.buffer[y][x]
		
		# Work-around: list() can't handle escape characters
		obj = [[self.sel+v+self.res]]
		self.graphics.draw(obj, x, y)
		
		self.selected = (x, y)
	
	def move(self, action):
		x_ = self.selected[0]
		y_ = self.selected[1]
		if action[1] == "h":
			v = 0 if action[2] == "e" else (x_-action[2])%self.w
			self.select(v, y_)
		elif action[1] == "j":
			v = self.h-1 if action[2] == "e" else (y_+action[2])%self.h
			self.select(x_, v)
		elif action[1] == "k":
			v = 0 if action[2] == "e" else (y_-action[2])%self.h
			self.select(x_, v)
		elif action[1] == "l":
			v = self.w-1 if action[2] == "e" else (x_+action[2])%self.w
			self.select(v, y_)
		else:
			action = None
			return self.Flow._BREAK
	
	def toggle_flag(self):
		s = self.graphics.buffer[self.selected[1]][self.selected[0]]
		fv = self.field[self.selected[1]][self.selected[0]]
		va = self.sel+self.graphics.mt+self.res
		vb = self.sel+self.fla+self.res
		vc = self.sel+" "+self.res
		if s == vc:
			return
		
		if s == va or s == vb:
			if self.selected in self.flags:
				self.flags.remove(self.selected)
				obj = [[self.graphics.mt]]
				self.graphics.draw(obj, *self.selected)
				tmp = self.selected
				self.selected = None
				self.select(*tmp)
				if fv:
					self.mines += 1
			else:
				self.flags += [self.selected]
				obj = [[self.fla]]
				self.graphics.draw(obj, *self.selected)
				tmp = self.selected
				self.selected = None
				self.select(*tmp)
				if fv:
					self.mines -= 1
		else:
			num = int(s[5:-5])
			x_ = self.selected[0]
			y_ = self.selected[1]
			pos = []
			mt = 0
			
			for i in range(max(y_-1, 0), min(y_+2, self.h)):
				for j in range(max(x_-1, 0), min(x_+2, self.w)):
					if self.graphics.buffer[i][j] == self.graphics.mt or self.graphics.buffer[i][j] == self.fla:
						if not self.graphics.buffer[i][j] == self.fla:
							pos += [(j, i)]
						mt += 1
			
			if num == mt:
				ori = self.selected
				for p in pos:
					self.select(*p)
					self.toggle_flag()
				self.select(*ori)
	
	def defuse(self):
		s = self.graphics.buffer[self.selected[1]][self.selected[0]]
		fv = self.field[self.selected[1]][self.selected[0]]
		va = self.sel+self.graphics.mt+self.res
		
		if s == va:
			if fv:
				return self.Flow._BREAK
			else:
				self.safe_sweep(*self.selected, True)
				return self.Flow._NORMAL
		else:
			try:
				num = int(s[5:-5])
				x_ = self.selected[0]
				y_ = self.selected[1]
				pos = []
				fs = 0
				
				for i in range(max(y_-1, 0), min(y_+2, self.h)):
					for j in range(max(x_-1, 0), min(x_+2, self.w)):
						if self.graphics.buffer[i][j] == self.fla:
							fs += 1
				
				if num == fs:
					tripped = False
					ori = self.selected
					for i in range(max(y_-1, 0), min(y_+2, self.h)):
						if tripped:
							break
						for j in range(max(x_-1, 0), min(x_+2, self.w)):
							if self.graphics.buffer[i][j] == self.graphics.mt:
								self.select(j, i)
								if self.defuse() is self.Flow._BREAK:
									tripped = True
							if tripped:
								break
					self.select(*ori)
					if tripped:
						return self.Flow._BREAK
					else:
						return self.Flow._NORMAL
			except:
				return self.Flow._NORMAL
	
	def cheat(self, action):
		if action[1] == "f":
			# First, clear incorrect flags
			for f in self.flags:
				if not self.field[f[1]][f[0]]:
					self.select(*f)
					self.toggle_flag()
			
			i = min(self.mines, action[2])
			while i > 0:
				found = False
				for y_ in range(self.h):
					if found:
						break
					for x_ in range(self.w):
						if found:
							break
						if self.field[y_][x_] and not (x_, y_) in self.flags:
							self.select(x_, y_)
							self.toggle_flag()
							i -= 1
							found = True
		elif action[1] == "d":
			i = action[2]
			while i > 0:
				found = False
				for y_ in range(self.h):
					if found:
						break
					for x_ in range(self.w):
						if found:
							break
						if not self.field[y_][x_] and self.graphics.buffer[y_][x_] == self.graphics.mt:
							self.select(x_, y_)
							self.defuse()
							i -= 1
							found = True
				if not found:
					break
	
	def parse_command(self, inp):
		if len(inp) == 0 or len(inp) > 3:
			return (self.Action._NO_ACTION, None, None)
		if inp[0] == "q":
			return (self.Action._FORCE_QUIT, None, None)
		if inp[0] == "f":
			return (self.Action._FLAG_ACTION, None, None)
		if inp[0] == "d":
			return (self.Action._DEFUSE_ACTION, None, None)
		if inp[0] == "h" or inp[0] == "j" or inp[0] == "k" or inp[0] == "l":
			if len(inp) == 1:
				return (self.Action._MOVE_ACTION, inp[0], 1)
			if inp[1] == "e":
				return (self.Action._MOVE_ACTION, inp[0], inp[1])
			try:
				return (self.Action._MOVE_ACTION, inp[0], int(inp[1]))
			except:
				return (self.Action._NO_ACTION, None, None)
		if inp[0] == "c":
			if inp[1] == "f" or inp[1] == "d":
				if len(inp) == 2:
					return (self.Action._CHEAT_ACTION, inp[1], 1)
				try:
					return (self.Action._CHEAT_ACTION, inp[1], int(inp[2]))
				except:
					return (self.Action._NO_ACTION, None, None)
		return (self.Action._NO_ACTION, None, None)
	
	def new_game(self):
		# Generate minefield
		self.field = [[False for _ in range(self.w)] for _ in range(self.h)]
		i = 0
		while i < self.mines:
			x = random.randrange(self.w)
			y = random.randrange(self.h)
			if not self.field[y][x]:
				self.field[y][x] = True
				i += 1
		
		# Guarantee connectivity (8 directions)
		# Maybe skip this
		
		# Give free 0 square
		x = random.randrange(self.w)
		y = random.randrange(self.h)
		
		while self.field[y][x] or self.num(x, y) > 0:
			x = random.randrange(self.w)
			y = random.randrange(self.h)
		
		self.safe_sweep(x, y)
		self.select(x, y)
		
		# Show initial board
		self.graphics.print_buffer()
		
		# Start game loop
		self.game_loop()
	
	def game_loop(self):
		action = None
		while True:
			# Parse commands
			inp = input("Bombs: {} > ".format(self.v_mines - len(self.flags))).split()
			action = self.parse_command(inp)
			
			if action[0] is self.Action._FORCE_QUIT:
				break
			
			if action[0] is self.Action._MOVE_ACTION:
				if self.move(action) is self.Flow._BREAK:
					break
			
			if action[0] is self.Action._FLAG_ACTION:
				self.toggle_flag()
			
			if action[0] is self.Action._DEFUSE_ACTION:
				if self.defuse() is self.Flow._BREAK:
					break
			
			if action[0] is self.Action._CHEAT_ACTION:
				self.cheat(action)
			
			# Check for victory
			if self.mines == 0 and self.v_mines == len(self.flags):
				break
			
			# Print changes
			self.graphics.print_buffer()
		
		# End screen
		msg = ""
		if action is None:
			msg = "An error occured"
		elif action[0] is self.Action._FORCE_QUIT:
			msg = "Game forced quit."
		elif self.mines == 0 and self.v_mines == len(self.flags):
			msg = "You won!"
		else:
			msg = "You lost"
			for y_ in range(self.h):
				for x_ in range(self.w):
					if self.field[y_][x_]:
						obj = [[self.min]]
						self.graphics.draw(obj, x_, y_)
		
		self.graphics.print_buffer()
		input(msg)



game = Game()
game.new_game()
