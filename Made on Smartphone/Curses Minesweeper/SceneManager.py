"""
This file is the central area for all Minesweeper scenes. The purose of
SceneManager is to evade circular import errors when two scenes need to
reference each other (such as during the changing between scenes.)
"""
from MenuScene import MenuScene
from NewGameScene import NewGameScene

def mk_MenuScene(game):
	"""Creates and returns a MenuScene."""
	return MenuScene(game)

def mk_NewGameScene(game):
	"""Creates and returns a NewGameScene."""
	return NewGameScene(game)
