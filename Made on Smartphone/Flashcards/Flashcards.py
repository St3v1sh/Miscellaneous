"""
This program was written on my smartphone.
This is a flashcard program. I made this to play around with python's
abilities to read files.
"""
from copy import deepcopy
from enum import Enum
from abc import ABC, abstractmethod
import os
import random

class Colors:
	_RESET = "\u001b[0m"
	_UL = "\u001b[4m"
	
	_BC = 48
	_TC = 38
	
	_BLACK = 0
	_WHITE = 231
	_GRAY = 250
	_BLUE = 33
	
	def esc(self, bt, col):
		return "\u001b[{};5;{}m".format(bt, col)

class Flow(Enum):
	_NORMAL = 0
	_BREAK = 1
	_CONTINUE = 2
	_RETURN = 3

class Graphics:
	def __init__(self):
		self.w = 60
		self.h = 29
		self.default_buffer = [[[" ", ""] for _ in range(self.w)] for _ in range(self.h)]
		self.buffer = deepcopy(self.default_buffer)
		self.C = Colors()  # For printing in color.
		
	def print_buffer(self):
		for line in self.buffer:
			for c in line:
				print(c[1]+c[0]+Colors._RESET, end="")
			print()
	
	def reset_buffer(self):
		self.buffer = deepcopy(self.default_buffer)
		
	def draw(self, obj, x, y):
		h = len(obj)
		for dy in range(h):
			w = len(obj[dy])
			self.buffer[y + dy][x:x+w] = obj[dy]
	
	def right_justify(self, obj):
		m = len(obj[0])
		for line in obj:
			if len(line) > m:
				m = len(line)
		return (obj, self.w-m)
	
	def to_obj(self, s):
		# 1-line string
		if isinstance(s, str):
			tmp = list(s)
			return [[[v, ""] for v in tmp]]
		elif isinstance(s, list):
			if len(s) < 2:
				return [[["?", ""]]]
			# Array of strings
			if isinstance(s[0], str) and isinstance(s[1], str):
				tmp = [list(v) for v in s]
				return [[[v, ""] for v in line] for line in tmp]
			# 1-line string and array of colors
			elif isinstance(s[0], str) and isinstance(s[1], list):
				tmp = list(s[0])
				temp = [[[v, ""] for v in tmp]]
				last = ""
				for i in range(len(tmp)):
					if i >= len(s[1]):
						temp[0][i][1] = last
					else:
						last = s[1][i]
						temp[0][i][1] = last
				return temp
			# Array of strings and 2D array of colors
			elif isinstance(s[0], list) and isinstance(s[1], list):
				if len(s[0]) < 1:
					return [[["?", ""]]]
				tmp = [list(v) for v in s[0]]
				temp = [[[v, ""] for v in line] for line in tmp]
				last = ""
				for i in range(len(tmp)):
					if i >= len(s[1]):
						for j in range(len(tmp[i])):
							temp[i][j][1] = last
					else:
						for j in range(len(tmp[i])):
							if j >= len(s[1][i]):
								temp[i][j][1] = last
							else:
								last = s[1][i][j]
								temp[i][j][1] = last
				return temp
		return [[["?", ""]]]

class Scene(ABC):
	@abstractmethod
	def loop(self):
		pass

class Game:
	def __init__(self, path):
		self.lc = "s"  # Last valid command.
		self.G = Graphics()  # For drawing.
		self.work_folder = path  # Folder where flashcards are stored.
		self.running = True
		
		self.scene = None  # Current scene.
	
	def start(self):
		self.change_scene(self.Menu_Scene(self))
		
		while self.running:
			self.scene.loop()
	
	def change_scene(self, scene):
		self.scene = scene
	
	def get_inp(self):
		return input("(%s) " % self.lc).strip()
	
	
	
	class Study_Scene(Scene):
		def __init__(self, g, path):
			self.g = g  # Game class.
			self.G = self.g.G  # Graphics class.
			self.f = []  # Flashcards.
			self.p = path  # Name of current set.
			self.ci = None  # Custom index sequence.
			self.s = False  # True if cards are shuffled.
			self.i = 0  # Current index in flashcards.
			self.t = True  # On term side if True, otherwise on definition side.
			
			# Prepare flashcards
			tmp = ["", ""]
			with open(self.p, "r") as f:
				for l in f:
					if self.t:
						tmp[0] = l[:-1]
					else:
						tmp[1] = l[:-1]
						self.f += [tmp[:]]
					self.t = not self.t
			self.t = True
			self.ci = [i for i in range(len(self.f))]
		
		def loop(self):
			inp = None
			
			# Initial drawing.
			self.G.reset_buffer()
			self.draw_card()
			self.G.print_buffer()
			
			while True:
				# User input.
				inp = self.g.get_inp()
				f = self.parse_inp(inp)
				if f is Flow._RETURN:
					return
				elif f is Flow._BREAK:
					break
				
				# Drawing.
				self.G.reset_buffer()
				self.draw_card()
				self.G.print_buffer()
			
			self.g.running = False
		
		def draw_card(self):
			# Decorations.
			self.draw_setup()
			
			# Page.
			c = ""
			ind = 0
			if not self.t:
				c = self.G.C.esc(self.G.C._BC, self.G.C._GRAY)
				c += self.G.C.esc(self.G.C._TC, self.G.C._BLACK)
				ind = 1
				s = " " * self.G.w
				obj = self.G.to_obj([s, [c]])
				for i in range(1, self.G.h-2):
					self.G.draw(obj, 0, i)
			
			# Distribute words into lines.
			ml = self.G.h-3
			mw = self.G.w
			lines = self.distr(ind)
			if len(lines) > ml:
				s = " ".join(lines[ml-1])
				sl = len(s)
				if sl + 1 < mw:
					lines[ml-1][-1] += " %s" % lines[ml][0]
					s = s + " %s" % lines[ml][0]
					sl = len(s)
				d = sl - mw
				lines[ml-1][-1] = lines[ml-1][-1][:-(d+3)] + "..."
			
			# Draw words.
			for i in range(min(len(lines), ml)):
				obj = self.G.to_obj([" ".join(lines[i]), [c]])
				self.G.draw(obj, 0, i+1)
		
		def distr(self, ind):
			words = self.f[self.ci[self.i]][ind].split(" ")
			l = 0
			lines = []
			line = []
			ml = self.G.w
			for i in range(len(words)):
				w = words[i]
				# Split up long words.
				if len(w) > ml:
					if l > 0:
						l += 1
					j = 0
					while j < len(w):
						jl = min(ml - l, len(w) - j)
						line += [w[j:j+jl]]
						j += jl
						l += jl
						if l == ml:
							lines += [line[:]]
							line = []
							l = 0
				# Make a new line if it's full.
				elif len(w) + l + 1 > ml:
					lines += [line[:]]
					line = [w]
					l = len(w)
				# Append to current line.
				else:
					line += [w]
					l += len(w) + 1
			if line is not []:
				lines += [line[:]]
			return lines
		
		def draw_setup(self):
			# Highlights
			c = self.G.C.esc(self.G.C._BC, self.G.C._WHITE)
			c += self.G.C.esc(self.G.C._TC, self.G.C._BLACK)
			s = " " * self.G.w
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, 0, 0)
			self.G.draw(obj, 0, self.G.h-2)
			
			# Top banner.
			s = "TERM" if self.t else "DEFINITION"
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, (self.G.w-len(s))//2, 0)
			
			# Bottom banner.
			s = "     {}/{}".format(self.i+1, len(self.f))
			if self.s:
				s += " (Shuffled)"
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, 0, self.G.h-2)
			s_ = os.path.splitext(self.p.split("/")[-1])[0]
			l = self.G.w - (len(s) + 6)
			if len(s_) > l:
				s_ = s_[:l-3] + '...'
			s_ += "     "
			obj = self.G.to_obj([s_, [c]])
			self.G.draw(*self.G.right_justify(obj), self.G.h-2)
			
			# Controls.
			obj = self.G.to_obj("     w: Flip, a: Prev, d: Next, s: Shuffle, q: Quit")
			self.G.draw(obj, 0, self.G.h-1)
		
		def parse_inp(self, inp_):
			inp = inp_.split()
			if len(inp) < 1:
				return self.parse_inp(self.g.lc)
			if len(inp) != 1:
				return Flow._NORMAL
			if inp[0] == "q":
				self.g.lc = "s"
				self.g.change_scene(self.g.Menu_Scene(self.g))
				return Flow._RETURN
			if inp[0] == "w":
				self.g.lc = inp_
				self.t = not self.t
				return Flow._NORMAL
			if inp[0] == "d":
				self.g.lc = "w"
				self.i = (self.i + 1) % len(self.f)
				self.t = True
				return Flow._NORMAL
			if inp[0] == "a":
				self.g.lc = "w"
				self.i = (self.i - 1) % len(self.f)
				self.t = True
				return Flow._NORMAL
			if inp[0] == "s":
				if self.s:
					self.ci = [i for i in range(len(self.f))]
				else:
					random.shuffle(self.ci)
				self.t = True
				self.s = not self.s
				return Flow._NORMAL
			return Flow._NORMAL
	
	
	
	class Menu_Scene(Scene):
		def __init__(self, g):
			self.g = g  # Game class.
			self.G = self.g.G  # Graphics class.
			self.cards_list = []  # Directory of available flashcards.
			self.p = 0  # Current page of flashcard selection.
			self.np = 0  # Total number of pages.
			self.s = 0  # Selected index of current page.
			self.pl = self.G.h-3  # Max number of flashcards per page in cards selection.
			
			fs = os.scandir(self.g.work_folder)
			for f in fs:
				if os.path.splitext(f.name)[1] == ".flashcards":
					self.cards_list += [[f.name, 0]]
			
			fs.close()
			
			for cards in self.cards_list:
				c = 0
				with open(self.g.work_folder+cards[0], "r") as f:
					for c, s in enumerate(f, 1):
						pass
				cards[1] = c//2
			
			self.np = (len(self.cards_list) + self.pl - 1) // self.pl
		
		def loop(self):
			if len(self.cards_list) == 0:
				print("No flashcards found in %s folder" % self.work_folder)
				self.g.running = False
				return
			
			inp = None
			
			# Initial drawing.
			self.G.reset_buffer()
			self.draw_sets()
			self.G.print_buffer()
			
			while True:
				# User input.
				inp = self.g.get_inp()
				f = self.parse_inp(inp)
				if f is Flow._RETURN:
					return
				elif f is Flow._BREAK:
					break
				
				# Drawing.
				self.G.reset_buffer()
				self.draw_sets()
				self.G.print_buffer()
			
			self.g.running = False
		
		def draw_sets(self):
			# Decorations.
			self.draw_setup()
			
			# Page.
			end = min(len(self.cards_list), (self.p+1)*self.pl)
			for i in range(self.p*self.pl, end):
				j = i - self.p*self.pl
				cards = self.cards_list[i]
				s = str(cards[1])+" flashcard(s)     "
				obj = self.G.to_obj(s)
				obj, x = self.G.right_justify(obj)
				self.G.draw(obj, x, j+1)
				s_ = os.path.splitext(cards[0])[0]
				l = self.G.w - (len(s) + 6)
				if len(s_) > l:
					s_ = s_[:l-3] + '...'
				obj = self.G.to_obj(s_)
				self.G.draw(obj, 5, j+1)
		
		def draw_setup(self):
			# Highlights
			c = self.G.C.esc(self.G.C._BC, self.G.C._WHITE) + self.G.C.esc(self.G.C._TC, self.G.C._BLACK)
			s = " " * self.G.w
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, 0, 0)
			self.G.draw(obj, 0, self.G.h-2)
			
			# Top banner.
			s = "     SETS"
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, 0, 0)
			s = "LENGTH     "
			obj = self.G.to_obj([s, [c]])
			self.G.draw(*self.G.right_justify(obj), 0)
			
			# Bottom banner.
			s = "     Page {}/{}".format(self.p+1, self.np)
			obj = self.G.to_obj([s, [c]])
			self.G.draw(obj, 0, self.G.h-2)
			s = self.g.work_folder+"     "
			obj = self.G.to_obj([s, [c]])
			self.G.draw(*self.G.right_justify(obj), self.G.h-2)
			
			# Selection arrow.
			obj = self.G.to_obj(">>>")
			self.G.draw(obj, 1, self.s+1)
			
			# Controls.
			obj = self.G.to_obj("     wasd: Move, m: Select, q: Quit")
			self.G.draw(obj, 0, self.G.h-1)
		
		def parse_inp(self, inp_):
			inp = inp_.split()
			if len(inp) < 1:
				return self.parse_inp(self.g.lc)
			if len(inp) != 1:
				return Flow._NORMAL
			if inp[0] == "q":
				self.g.lc = inp_
				return Flow._BREAK
			if inp[0] == "s":
				self.g.lc = inp_
				w = len(self.cards_list) % self.pl if self.p == self.np-1 else self.pl
				self.s = (self.s + 1) % w
				return Flow._NORMAL
			if inp[0] == "w":
				self.g.lc = inp_
				w = len(self.cards_list) % self.pl if self.p == self.np-1 else self.pl
				self.s = (self.s - 1) % w
				return Flow._NORMAL
			if inp[0] == "d":
				self.g.lc = inp_
				self.p = (self.p + 1) % self.np
				self.s = 0
				return Flow._NORMAL
			if inp[0] == "a":
				self.g.lc = inp_
				self.p = (self.p - 1) % self.np
				self.s = 0
				return Flow._NORMAL
			if inp[0] == "m":
				self.g.lc = "w"
				path = self.g.work_folder + self.cards_list[self.p*self.pl + self.s][0]
				self.g.change_scene(self.g.Study_Scene(self.g, path))
				return Flow._RETURN
			return Flow._NORMAL



game = Game("./Sets/")
game.start()
