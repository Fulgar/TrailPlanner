# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: PROJECT
# Due Date: December 2, 2019
# Signature: Jason James
# Score: _________________

# AlgoContainer Class is used to contain relevant algorithm fields for easier data logistics
class AlgoContainer:

	# Constructor
	def __init__(self, canvas, currentX, currentY, tiles, guiTiles, rightHandElements, startX, goalX, closed, open, algoFields):
		self.canvas = canvas
		self.currentX = currentX
		self.currentY = currentY
		self.tiles = tiles
		self.guiTiles = guiTiles
		self.rightHandElements = rightHandElements
		self.startX = startX
		self.goalX = goalX
		self.closed = closed
		self.open = open
		self.algoFields = algoFields
