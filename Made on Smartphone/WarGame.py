"""
This program was written on my smartphone.
To test out using the IDE further, this program was written. It plays
the war card game.
"""
import random
from enum import Enum
from copy import deepcopy

class Graphics:
	def __init__(self):
		self.len_x = 58
		self.len_y = 27
		self.default_buffer = [[" " for _ in range(self.len_x)] for _ in range(self.len_y)]
		self.buffer = deepcopy(self.default_buffer)
		self.border_x = ["+"] + ["~" for _ in range(self.len_x)] + ["+"]
		self.border_y = ["|"] * self.len_y
		
	def print_buffer(self):
		res = self.set_border()
		for line in res:
			print("".join(line))
	
	def reset_buffer(self):
		self.buffer = deepcopy(self.default_buffer)
	
	def set_border(self):
		res = [[self.border_y[i]] + self.buffer[i] + [self.border_y[i]] for i in range(self.len_y)]
		return [self.border_x] + res + [self.border_x]
		
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
		return (obj, self.len_x-m, y)
	
	def to_obj(self, s):
		return [list(s)]
	
	def arr_to_obj(self, arr):
		return [list(s) for s in arr]

class Game:
	class Winner(Enum):
		_no_winner = 0
		_p_a_winner = 1
		_p_b_winner = 2
		_tie_winner = 3
	
	class Flow(Enum):
		_normal = 0
		_break = 1
		_continue = 2
	
	def __init__(self, deck):
		self._no_winner = self.Winner._no_winner
		self._p_a_winner = self.Winner._p_a_winner
		self._p_b_winner = self.Winner._p_b_winner
		self._tie_winner = self.Winner._tie_winner
		
		self._normal = self.Flow._normal
		self._break = self.Flow._break
		self._continue = self.Flow._continue
		
		self.default_deck = deck[:]
		self.deck = []
		self.p_a_grave = []
		self.p_b_grave = []
		self.p_a = []
		self.p_b = []
		self.p_a_play = []
		self.p_b_play = []
		self.graphics = Graphics()
		
		self.troops_text = "# of troops: "
		self.grave_text = "Grave: "
		self.win_sprite = "<======}~+"
		self.loss_sprite = "+~{======>"
		self.tie_sprite = "+~{======>!!<======}~+"
		self.victory_sprite = [
			"       ..",
			"    o^/()\\^o",
			" o.^|\\/\\/\\/|^.o",
			"o\\*`'.\\||/.'`*/o",
			" \\/\\\\\\\\\\/////\\/",
			"  {><><[]><><}",
			"   \"\"\"\"\"\"\"\"\"\""
		]
		self.defeat_sprite = [
			"                o^/()\\^o",
			"       /`    o.^|\\/\\/\\/|^.o",
			"\\.....//----o\\*`'.\\|-------------------.",
			"/`````\\\\-----\\/\\\\\\\\\\--------------------`",
			"       \\.     {><><[]><><}",
			"               \"\"\"\"\"\"\"\"\"\""
		]
	
	def shuffle(self, arr):
		random.shuffle(arr)
	
	def new_game(self):
		self.deck = self.default_deck[:]
		self.shuffle(self.deck)
		
		for i in range(len(self.deck)):
			if i%2:
				self.p_b = [self.deck[i]] + self.p_b
			else:
				self.p_a = [self.deck[i]] + self.p_a
		self.deck = []
		
		obj = self.graphics.to_obj("War card game is starting!")
		self.graphics.draw(obj, 16, 12)
		
		obj = self.graphics.to_obj("Press enter to continue.")
		self.graphics.draw(obj, 17, 14)
		
		self.graphics.print_buffer()
		self.graphics.reset_buffer()
		
		input("Press enter.")
		
		self.basic_graphics()
		self.graphics.print_buffer()
		self.graphics.reset_buffer()
	
	def draw_cards(self):
		self.p_a_play += [self.p_a.pop(0)]
		self.p_b_play += [self.p_b.pop(0)]
	
	def clear_field(self, to):
		to += self.p_a_play + self.p_b_play
		self.p_a_play, self.p_b_play = [], []
	
	def get_winner(self):
		if len(self.p_a) == len(self.p_b) == 0 == len(self.p_a_grave) == len(self.p_b_grave):
			return self._tie_winner
		elif len(self.p_a) == 0 == len(self.p_a_grave):
			return self._p_b_winner
		elif len(self.p_b) == 0 == len(self.p_b_grave):
			return self._p_a_winner
		else:
			return self._no_winner
	
	def basic_graphics(self):
		# p_a
		tmp = self.troops_text+str(len(self.p_a))
		obj = self.graphics.to_obj(tmp)
		self.graphics.draw(obj, 0, 0)
		
		tmp = self.grave_text+str(len(self.p_a_grave))
		obj = self.graphics.to_obj(tmp)
		self.graphics.draw(obj, 0, 1)
		
		# p_b
		tmp = self.troops_text+str(len(self.p_b))
		obj = self.graphics.to_obj(tmp)
		self.graphics.draw(*self.graphics.right_justify(obj, 26))
		
		tmp = self.grave_text+str(len(self.p_b_grave))
		obj = self.graphics.to_obj(tmp)
		self.graphics.draw(*self.graphics.right_justify(obj, 25))
	
	def needs_shuffle(self):
		a = len(self.p_a) == 0 and len(self.p_a_grave) > 0
		b = len(self.p_b) == 0 and len(self.p_b_grave) > 0
		
		return (a, b)
	
	def player_shuffle(self, a, b):
		if a:
			self.shuffle(self.p_a_grave)
			self.p_a += self.p_a_grave
			self.p_a_grave = []
		if b:
			self.shuffle(self.p_b_grave)
			self.p_b += self.p_b_grave
			self.p_b_grave = []
	
	def display_shuffle_text(self, a, b):
		if a or b:
			input("Shuffling...")
			
			self.basic_graphics()
			obj = self.graphics.to_obj("Shuffled")
			self.graphics.draw(obj, 25, 13)
			
			self.graphics.print_buffer()
			self.graphics.reset_buffer()
	
	def draw_swords(self, v):
		# Put cards into proper grave, unless there's a war
		if v > 0:
			obj = self.graphics.to_obj(self.win_sprite)
			self.graphics.draw(obj, 19, 13)
		elif v < 0:
			obj = self.graphics.to_obj(self.loss_sprite)
			self.graphics.draw(obj, 29, 13)
		else:
			obj = self.graphics.to_obj(self.tie_sprite)
			self.graphics.draw(obj, 18, 13)
	
	def draw_field(self, ap, bp, modified = False):
		nm = not modified
		
		a = ap[-1]
		b = bp[-1]
		
		la = len(ap)
		lb = len(bp)
		las = len(str(la - 1)) if nm else len(str(la))
		
		# Check if there's a war
		tmp = str(a)
		obj = self.graphics.to_obj(tmp)
		obj_ = self.graphics.to_obj(str(b))
		if la == 1 and nm:
			# If not, draw normally
			self.graphics.draw(obj, 27-(len(tmp))+1, 12)
			self.graphics.draw(obj_, 30, 14)
		else:
			# If so, show the stakes
			if nm:
				self.graphics.draw(obj, 27-(len(tmp))+1, 11)
				self.graphics.draw(obj_, 30, 15)
			
			tmp = str(la - 1) if nm else str(la)
			obj = self.graphics.to_obj(tmp+">")
			self.graphics.draw(obj, 27-las+1, 12)
			
			tmp = str(lb - 1) if nm else str(lb)
			obj = self.graphics.to_obj("<"+tmp)
			self.graphics.draw(obj, 30, 14)
	
	def print_end(self):
		res = self.get_winner()
		if res is self._no_winner:
			obj = self.graphics.to_obj("Game  quit")
			self.graphics.draw(obj, 24, 18)
		elif res is self._p_a_winner:
			obj = self.graphics.to_obj("You won!")
			self.graphics.draw(obj, 25, 18)
			
			obj = self.graphics.to_obj("Out of troops!")
			self.graphics.draw(*self.graphics.right_justify(obj, 24))
			
			obj = self.graphics.arr_to_obj(self.victory_sprite)
			self.graphics.draw(obj, 21, 3)
		elif res is self._p_b_winner:
			obj = self.graphics.to_obj("You lost..")
			self.graphics.draw(obj, 24, 18)
			
			obj = self.graphics.to_obj("Out of troops!")
			self.graphics.draw(obj, 0, 2)
			
			obj = self.graphics.arr_to_obj(self.defeat_sprite)
			self.graphics.draw(obj, 9, 3)
		else:
			obj = self.graphics.to_obj("Tied  game")
			self.graphics.draw(obj, 24, 18)
			
			obj = self.graphics.to_obj("Out of troops!")
			self.graphics.draw(*self.graphics.right_justify(obj, 24))
			
			obj = self.graphics.to_obj("Out of troops!")
			self.graphics.draw(obj, 0, 2)
	
	def parse_command(self, inp):
		# Low-effort and inefficient.. but its just a few commands!
		if len(inp) > 0:
			if inp[0] == "q":
				return self._break
			elif inp[0] == "peek":
				an = self.p_a[0] if len(self.p_a) > 0 else None
				bn = self.p_b[0] if len(self.p_b) > 0 else None
				print("a: {}, b: {}".format(an, bn))
				return self._continue
			elif inp[0] == "set" and len(inp) >= 3:
				selected = None
				if inp[1] == "a":
					selected = self.p_a
				elif inp[1] == "b":
					selected = self.p_b
				try:
					selected[0] = int(inp[2])
				except:
					pass
			elif inp[0] == "win":
				self.p_b = []
				self.p_b_grave = []
				return self._break
			elif inp[0] == "lose":
				self.p_a = []
				self.p_a_grave = []
				return self._break
		return self._normal
	
	def start_game_loop(self):
		inp = None
		while self.get_winner() is self._no_winner:
			# Commands
			inp = input().split()
			flow = self.parse_command(inp)
			
			if flow is self._break:
				break
			elif flow is self._continue:
				continue
			
			# Game logic
			
			# Draw cards
			self.draw_cards()
			
			a = self.p_a_play[-1]
			b = self.p_b_play[-1]
			v = a - b
			
			self.draw_swords(v)
			self.draw_field(self.p_a_play, self.p_b_play)
			
			if a == b:
				# War happened! Each side puts in 3 cards
				i = 0
				shuffled = False
				while i < 3:
					# Check if shuffling is needed
					need_shuffle = self.needs_shuffle()
					self.player_shuffle(*need_shuffle)
					if need_shuffle[0] or need_shuffle[1]:
						shuffled = True
					
					# Check if game is over
					if not self.get_winner() is self._no_winner:
						break
					
					# Put in a card for each side
					self.draw_cards()
					
					# Increment
					i += 1
				
				if shuffled:
					obj = self.graphics.to_obj("Shuffled during war.")
					self.graphics.draw(obj, 19, 18)
			
			# Put cards to grave, unless there's a war
			if a > b:
				self.clear_field(self.p_a_grave)
			elif a < b:
				self.clear_field(self.p_b_grave)
			
			# Print graphics
			self.basic_graphics()
			self.graphics.print_buffer()
			self.graphics.reset_buffer()
			
			# Shuffle if needed
			need_shuffle = self.needs_shuffle()
			self.player_shuffle(*need_shuffle)
			self.display_shuffle_text(*need_shuffle)
		
		# Aftergame stuff
		if not (inp == ["q"] or inp == ["win"] or inp == ["lose"]):
			input("Game ended.")
		
		self.basic_graphics()
		self.print_end()
		
		# Check if there was a war
		if len(self.p_a_play) > 0:
			self.draw_swords(0)
			
			# Don't print field if player ran out of cards during a war
			war = len(self.p_a_play) % 4 != 0
			self.draw_field(self.p_a_play, self.p_b_play, war)
		
		self.graphics.print_buffer()
		self.graphics.reset_buffer()
		
		input()



#deck = [(i//4)+1 for i in range(40)]
deck = [((i//4)+1) * 10 for i in range(40)]

# Testing decks
#deck = [1 for _ in range(22)]
#deck = [(i//5)+1 for i in range(10)]
#deck = [(i//10)+1 for i in range(30)]

game = Game(deck)
game.new_game()
game.start_game_loop()
