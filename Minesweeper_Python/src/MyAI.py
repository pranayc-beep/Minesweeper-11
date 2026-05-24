# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.X = startX
		self.Y = startY
		self.covered = set((x,y) for x in range(colDimension) for y in range(rowDimension))
		if (startX, startY) in self.covered:
			self.covered.remove((startX, startY))
		self.flags = set()
		self.moves = []
		self.safe = set()
		self.board = {}


	def getNeighbors(self, x, y):
		dx = [-1, 0, 1]
		dy = [-1, 0, 1]
		neighbors = []
		for i in dx:
			for j in dy:
				if (i == 0 and j == 0):
					continue
				newX = x + i
				newY = y + j
				if (0 <= newX < self.colDimension and 0 <= newY < self.rowDimension):
					neighbors.append((newX, newY))
		return neighbors
	
	def getAction(self, number: int) -> "Action Object":
		# if(number == 0):
		# 	self.covered.remove((self.X, self.Y))
		# 	self.safe.update((x, y) for x, y in self.getNeighbors(self.X, self.Y) if (x, y) in self.covered)
		# 	return Action(AI.Action.UNCOVER, self.X, self.Y)
		if number != -1:
			self.board[(self.X, self.Y)] = number

		if(self.safe):
			self.X, self.Y = self.safe.pop()
			return Action(AI.Action.UNCOVER, self.X, self.Y)
		
		if not self.moves:
			for (cx, cy), hint in self.board.items():
				neighbors = self.getNeighbors(cx, cy)
				covered_neighbors = [n for n in neighbors if n in self.covered]
				flagged_neighbors = [n for n in neighbors if n in self.flags]

				if hint == len(flagged_neighbors) + len(covered_neighbors) and covered_neighbors:
					for covered in covered_neighbors:
						if covered in self.covered:
							self.flags.add(covered)
							self.covered.remove(covered)
							self.moves.append(Action(AI.Action.FLAG, covered[0], covered[1]))

				elif hint == len(flagged_neighbors) and covered_neighbors:
					for covered in covered_neighbors:
						if covered in self.covered:
							self.covered.remove(covered)
							self.moves.append(Action(AI.Action.UNCOVER, covered[0], covered[1]))

		if not(self.moves):
			boundary_cells = {}
			for (cx, cy), hint in self.board.items():
				neighbors = self.getNeighbors(cx, cy)
				covered_neighbors = [n for n in neighbors if n in self.covered]
				if covered_neighbors:
					flags = [n for n in neighbors if n in self.flags]
					boundary_cells[(cx, cy)] = covered_neighbors
			for cell, covered_neighbors in boundary_cells.items():
				hint = self.board[cell]
				flags = [n for n in self.getNeighbors(cell[0], cell[1]) if n in self.flags]
				if hint == len(flags) + len(covered_neighbors):
					for covered in covered_neighbors:
						if covered in self.covered:
							self.flags.add(covered)
							self.covered.remove(covered)
							self.moves.append(Action(AI.Action.FLAG, covered[0], covered[1]))

				elif hint == len(flags):
					for covered in covered_neighbors:
						if covered in self.covered:
							self.covered.remove(covered)
							self.moves.append(Action(AI.Action.UNCOVER, covered[0], covered[1]))

		if (len(self.flags) == self.totalMines and not self.moves):
			for covered in list(self.covered):
				self.covered.remove(covered)
				self.moves.append(Action(AI.Action.UNCOVER, covered[0], covered[1]))

		if self.moves:
			next_move = self.moves.pop(0)
			if next_move.getMove() == AI.Action.UNCOVER:
				self.X, self.Y = next_move.getX(), next_move.getY()
			return next_move
		
		if(not self.covered):
			return Action(AI.Action.LEAVE)
		
		guess = self.covered.pop()
		self.X, self.Y = guess[0], guess[1]
		return Action(AI.Action.UNCOVER, self.X, self.Y)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
