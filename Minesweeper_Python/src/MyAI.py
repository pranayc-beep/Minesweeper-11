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
		if number != -1:
			self.board[(self.X, self.Y)] = number
		
		if self.safe:
			self.X, self.Y = self.safe.pop()
			return Action(AI.Action.UNCOVER, self.X, self.Y)
		
		if self.moves:
			next_move = self.moves.pop(0)
			if next_move.getMove() == AI.Action.UNCOVER:
				self.X, self.Y = next_move.getX(), next_move.getY()
			return next_move

		for (cx, cy), hint in self.board.items():
			neighbors = self.getNeighbors(cx, cy)
			cov = [n for n in neighbors if n in self.covered]
			flg = [n for n in neighbors if n in self.flags]

			if hint == len(flg) + len(cov) and cov:
				for c in cov:
					if c in self.covered:
						self.flags.add(c)
						self.covered.remove(c)
						self.moves.append(Action(AI.Action.FLAG, c[0], c[1]))
			elif hint == len(flg) and cov:
				for c in cov:
					if c in self.covered:
						self.safe.add(c)
						self.covered.remove(c)

		if self.safe:
			self.X, self.Y = self.safe.pop()
			return Action(AI.Action.UNCOVER, self.X, self.Y)
		if self.moves:
			return self.moves.pop(0)

		boundary = {}
		for (cx, cy), hint in self.board.items():
			neighbors = self.getNeighbors(cx, cy)
			cov = set(n for n in neighbors if n in self.covered)
			if cov:
				flg = set(n for n in neighbors if n in self.flags)
				boundary[(cx, cy)] = (cov, hint - len(flg))

		for cellA, (covA, effA) in boundary.items():
			for cellB, (covB, effB) in boundary.items():
				if cellA == cellB: continue
				
				if covA.issubset(covB) and len(covB) > len(covA):
					diff_cov = covB - covA
					diff_eff = effB - effA

					if diff_eff == 0:
						for c in diff_cov:
							if c in self.covered:
								self.safe.add(c)
								self.covered.remove(c)
					
					elif diff_eff == len(diff_cov):
						for c in diff_cov:
							if c in self.covered:
								self.flags.add(c)
								self.covered.remove(c)
								self.moves.append(Action(AI.Action.FLAG, c[0], c[1]))

		if self.safe:
			self.X, self.Y = self.safe.pop()
			return Action(AI.Action.UNCOVER, self.X, self.Y)
		if self.moves:
			return self.moves.pop(0)

		if len(self.flags) == self.totalMines and self.covered:
			for c in list(self.covered):
				self.safe.add(c)
				self.covered.remove(c)
			self.X, self.Y = self.safe.pop()
			return Action(AI.Action.UNCOVER, self.X, self.Y)

		if not self.covered:
			return Action(AI.Action.LEAVE)

		frontier = set()
		for cov, eff in boundary.values():
			frontier.update(cov)
		
		non_frontier = self.covered - frontier
		mines_left = self.totalMines - len(self.flags)
		global_risk = mines_left / len(self.covered) if len(self.covered) > 0 else 1.0
		best_frontier_guess = None
		best_frontier_risk = 1.0
		
		if boundary:
			cell_risk = {}
			for (cx, cy), (cov, eff) in boundary.items():
				risk = eff / len(cov) if len(cov) > 0 else 1.0
				for c in cov:
					if c not in cell_risk or risk > cell_risk[c]:
						cell_risk[c] = risk
			
			if cell_risk:
				best_frontier_guess = min(cell_risk, key=cell_risk.get)
				best_frontier_risk = cell_risk[best_frontier_guess]

		if non_frontier and global_risk <= best_frontier_risk:
			corners = {(0, 0), (self.colDimension - 1, 0), 
					   (0, self.rowDimension - 1), (self.colDimension - 1, self.rowDimension - 1)}
			available_corners = non_frontier.intersection(corners)
			
			if available_corners:
				guess = available_corners.pop()
			else:
				guess = non_frontier.pop()
				
			self.covered.remove(guess)
			self.X, self.Y = guess[0], guess[1]
			return Action(AI.Action.UNCOVER, self.X, self.Y)
			
		elif best_frontier_guess:
			self.covered.remove(best_frontier_guess)
			self.X, self.Y = best_frontier_guess[0], best_frontier_guess[1]
			return Action(AI.Action.UNCOVER, self.X, self.Y)

		guess = self.covered.pop()
		self.X, self.Y = guess[0], guess[1]
		return Action(AI.Action.UNCOVER, self.X, self.Y)