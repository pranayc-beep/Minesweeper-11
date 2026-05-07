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
		self.covered.remove((startX, startY))
		self.flags = set()
		self.moves = []

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
				if (0 <= newX < self.rowDimension and 0 <= newY < self.colDimension):
					neighbors.append((newX, newY))
		return neighbors
	
	def getAction(self, number: int) -> "Action Object":
		if(number == 0):
			#self.covered.remove((self.X, self.Y))
			return Action(AI.Action.UNCOVER, self.X, self.Y)
		
		neighbors = self.getNeighbors(self.X, self.Y)
		covered_neighbors = [n for n in neighbors if n in self.covered]
		flagged_neighbors = [n for n in neighbors if n in self.flags]
		if(number == len(flagged_neighbors) + len(covered_neighbors)):
			for covered in covered_neighbors:
				self.flags.add(covered)
				self.covered.remove(covered)
				self.moves.append(Action(AI.Action.FLAG, covered[0], covered[1]))

		elif(number == len(flagged_neighbors) and covered_neighbors):
			for covered in covered_neighbors:
				self.covered.remove(covered)
				self.moves.append(Action(AI.Action.UNCOVER, covered[0], covered[1]))

		elif (len(self.flags) == self.totalMines):
			for covered in self.covered:
				self.covered.remove(covered)
				self.moves.append(Action(AI.Action.UNCOVER, covered[0], covered[1]))

		if self.moves:
			self.X, self.Y = self.moves[0].getX(), self.moves[0].getY()
			return self.moves.pop(0)
		
		if(not self.covered):
			return Action(AI.Action.LEAVE)
		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
