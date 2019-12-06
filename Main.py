# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: PROJECT
# Due Date: December 2, 2019
# Signature: Jason James
# Score: _________________

from tkinter import *
from TileType import *
from Tile import *
import random
from AlgoContainer import *

HEURISTIC_SCALAR = 100  # Used to scale h-val

# Color constant fields
COLOR_PATH = "#B5651D"
COLOR_TREES_VERYLIGHT = "#b0ff78"
COLOR_TREES_LIGHT = "#6aff00"
COLOR_TREES_MEDIUM = "#429e00"
COLOR_TREES_HEAVY = "#235400"
COLOR_TREES_VERYHEAVY = "#122b00"
COLOR_ROCKS = "gray"

# Used to store future canvas ID's of outline boxes as a global variable
startOutlineID = None
goalOutlineID = None


# Driver method
def main():
	# Window Data
	root = Tk()
	root.title("Trail Planner")
	root.geometry('1000x750')

	# Canvas Data
	canvasWidth = 1000
	canvasHeight = 750
	canvas = Canvas(root, height=canvasHeight, width=canvasWidth, bg="lightgray")

	# Create grid lines
	gridVertLines = []
	gridHortLines = []
	coord = 0
	while coord <= 750:
		gridVertLines.append(canvas.create_line(coord, 0, coord, 750, fill="black"))
		gridHortLines.append(canvas.create_line(0, coord, 750, coord, fill="black"))
		coord += 75

	# Create 2D grid table
	tiles = [None] * 10
	for i in range(len(tiles)):
		tiles[i] = [None] * 10
		for j in range(len(tiles[i])):
			rockRand = random.randint(0, 9)
			if rockRand == 0:
				tiles[i][j] = Tile(TileType.ROCKS)
			else:
				treeRand = TileType(random.randint(1, 5))
				tiles[i][j] = Tile(treeRand)
		# 	print(tiles[i][j].getType())
		# print("\n")

	# Randomly set start position at top of map
	startX = random.randint(0, 9)
	tiles[0][startX] = Tile(TileType.PATH)
	startOutline = canvas.create_rectangle(startX * 75, 0, (startX * 75) + 75, 75, outline="blue", width=4)
	global startOutlineID
	startOutlineID = startOutline

	# Randomly set goal position at bottom of map
	goalX = random.randint(0, 9)
	tiles[9][goalX] = Tile(TileType.PATH)
	goalOutline = canvas.create_rectangle(goalX * 75, 675, (goalX * 75) + 75, 750, outline="blue", width=4)
	global goalOutlineID
	goalOutlineID = goalOutline

	# Create canvas visual of tiles grid table
	guiTiles = [None] * 10
	for i in range(len(tiles)):
		guiTiles[i] = [None] * 10
		for j in range(len(tiles[i])):
			tile = tiles[i][j]
			tileType = tile.getType()
			x1 = j * 75
			y1 = i * 75
			x2 = x1 + 75
			y2 = y1 + 75
			if tileType is TileType.TREES_VERYLIGHT:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TREES_VERYLIGHT)
			elif tileType is TileType.TREES_LIGHT:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TREES_LIGHT)
			elif tileType is TileType.TREES_MEDIUM:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TREES_MEDIUM)
			elif tileType is TileType.TREES_HEAVY:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TREES_HEAVY)
			elif tileType is TileType.TREES_VERYHEAVY:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TREES_VERYHEAVY)
			elif tileType is TileType.ROCKS:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_ROCKS)
			elif tileType is TileType.PATH:
				guiTiles[i][j] = canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PATH)
			else:
				print("ERROR: Invalid TileType value given @ tile grid", ("(" + str(i) + ", " + str(j) + ")"))

	# Raise outlines' layers above tiles' layers
	canvas.tag_raise(startOutline)
	canvas.tag_raise(goalOutline)

	# A* Algorithm Fields
	g = 0  # Total cost to get from start position to current position
	h = (abs(0 - 9) + abs(startX - goalX)) * HEURISTIC_SCALAR  # Represents the heuristic value distance to end goal
	f = g + h  # Represents the sum of g and h
	algoFields = [g, h, f]

	# Create Right-Hand Side Display Elements
	rightHandElements = []
	centerRight = 750 + 250/2

	# Display Program Title
	title = "Forest Trail Planner"
	rightHandElements.append(canvas.create_text(centerRight, 50, anchor=CENTER, text=title, font=("Purisa", 14)))

	# Display Dynamic A* Algorithm fields
	gLabel = canvas.create_text(800, 200, anchor=NW, text="G: \t" + str(g), font=("Purisa", 12))
	hLabel = canvas.create_text(800, 250, anchor=NW, text="H: \t" + str(h), font=("Purisa", 12))
	fLabel = canvas.create_text(800, 300, anchor=NW, text="F: \t" + str(f), font=("Purisa", 12))
	rightHandElements.append(gLabel)
	rightHandElements.append(hLabel)
	rightHandElements.append(fLabel)

	# Display "Next" button
	button = Button(text="Next", anchor=CENTER, font=("Purisa", 12))
	button.configure(width=10, activebackground="#33B5E5", relief=FLAT)
	buttonWindow = canvas.create_window(centerRight, 150, anchor=CENTER, window=button)
	rightHandElements.append(buttonWindow)

	# Display divider line
	rightHandElements.append(canvas.create_line(750, 375, 1000, 375, fill="black"))

	# Display "KEY" label
	keyLabel = canvas.create_text(centerRight, 390, anchor=CENTER, text="KEY", font=("Purisa", 13))
	rightHandElements.append(keyLabel)

	# Display color examples
	keyTREES_VERYLIGHT = canvas.create_rectangle(780, 440, 800, 460, fill=COLOR_TREES_VERYLIGHT)
	keyTREES_LIGHT = canvas.create_rectangle(780, 480, 800, 500, fill=COLOR_TREES_LIGHT)
	keyTREES_MEDIUM = canvas.create_rectangle(780, 520, 800, 540, fill=COLOR_TREES_MEDIUM)
	keyTREES_HEAVY = canvas.create_rectangle(780, 560, 800, 580, fill=COLOR_TREES_HEAVY)
	keyTREES_VERYHEAVY = canvas.create_rectangle(780, 600, 800, 620, fill=COLOR_TREES_VERYHEAVY)
	keyROCKS = canvas.create_rectangle(780, 640, 800, 660, fill=COLOR_ROCKS)
	keyPATH = canvas.create_rectangle(780, 680, 800, 700, fill=COLOR_PATH)
	rightHandElements.extend([keyTREES_VERYLIGHT, keyTREES_LIGHT, keyTREES_MEDIUM, keyTREES_HEAVY, keyTREES_VERYHEAVY])
	rightHandElements.extend(([keyPATH, keyROCKS]))

	# Display corresponding labels for color tiles
	keyLabelTREES_VERYLIGHT = canvas.create_text(805, 450, anchor=W, text="Very Light Trees", font=("Purisa", 8))
	keyLabelTREES_LIGHT = canvas.create_text(805, 490, anchor=W, text="Light Trees", font=("Purisa", 8))
	keyLabelTREES_MEDIUM = canvas.create_text(805, 530, anchor=W, text="Medium Trees", font=("Purisa", 8))
	keyLabelTREES_HEAVY = canvas.create_text(805, 570, anchor=W, text="Heavy Trees", font=("Purisa", 8))
	keyLabelTREES_VERYHEAVY = canvas.create_text(805, 610, anchor=W, text="Very Heavy Trees", font=("Purisa", 8))
	keyLabelROCKS = canvas.create_text(805, 650, anchor=W, text="Rocks", font=("Purisa", 8))
	keyLabelPATH = canvas.create_text(805, 690, anchor=W, text="Path", font=("Purisa", 8))
	rightHandElements.extend([keyLabelTREES_VERYLIGHT, keyLabelTREES_LIGHT, keyLabelTREES_MEDIUM, keyLabelTREES_HEAVY])
	rightHandElements.extend(([keyLabelTREES_VERYHEAVY, keyLabelPATH, keyLabelROCKS]))

	# Display dotted lines to divide KEY table
	rightHandElements.append(canvas.create_line(centerRight + 25, 435, centerRight + 25, 700, dash=(3, 1), fill="black"))
	rightHandElements.append(canvas.create_line(780, 435, 990, 435, dash=(3, 1), fill="black"))

	# Display table labels
	keyNodeNameLabel = canvas.create_text(805, 420, anchor=W, text="Density Node", font=("Purisa", 8))
	keyCostLabel = canvas.create_text(centerRight + 30, 420, anchor=W, text="Cost to Clear Path", font=("Purisa", 8))
	rightHandElements.extend([keyNodeNameLabel, keyCostLabel])

	# Display cost column
	keyCostTREES_VERYLIGHT = canvas.create_text(centerRight + 30, 450, anchor=W, text="$100", font=("Purisa", 8))
	keyCostTREES_LIGHT = canvas.create_text(centerRight + 30, 490, anchor=W, text="$150", font=("Purisa", 8))
	keyCostTREES_MEDIUM = canvas.create_text(centerRight + 30, 530, anchor=W, text="$200", font=("Purisa", 8))
	keyCostTREES_HEAVY = canvas.create_text(centerRight + 30, 570, anchor=W, text="$250", font=("Purisa", 8))
	keyCostTREES_VERYHEAVY = canvas.create_text(centerRight + 30, 610, anchor=W, text="$300", font=("Purisa", 8))
	keyCostTREES_ROCKS = canvas.create_text(centerRight + 30, 650, anchor=W, text="$1000", font=("Purisa", 8))
	keyCostTREES_PATH = canvas.create_text(centerRight + 30, 690, anchor=W, text="$0", font=("Purisa", 8))
	rightHandElements.extend([keyCostTREES_VERYLIGHT, keyCostTREES_LIGHT, keyCostTREES_MEDIUM, keyCostTREES_HEAVY])
	rightHandElements.extend([keyCostTREES_VERYHEAVY, keyCostTREES_ROCKS, keyCostTREES_PATH])

	# Initiate open and closed lists
	open = []
	closed = []

	# Holds all data that is required by the solve() method for A* Algorithm
	algoContainer = AlgoContainer(canvas, startX, 0, tiles, guiTiles, rightHandElements, startX, goalX, closed, open, algoFields)

	# Bind button's action to call solve method with algoContainer as argument
	button.configure(command=lambda: solve(algoContainer))

	# Display all canvas elements
	canvas.pack()

	mainloop()


# Completes one step in A* Path-finding algorithm
def solve(algoData):
	coordString = str("[" + str(algoData.currentY) + ", " + str(algoData.currentX) + "]")
	print("Previous Coord: ", coordString)
	if algoData.currentX == algoData.goalX and algoData.currentY == 9:
		print("PATH COMPLETE")
	else:
		# Get Neighbors
		neighbors = []
		for i in range(len(algoData.tiles)):
			for j in range(len(algoData.tiles[i])):
				if abs(algoData.currentX - j) == 1 and algoData.currentY == i:
					neighbors.append([i, j])
				elif abs(algoData.currentY - i) == 1 and algoData.currentX == j:
					neighbors.append([i, j])
				else:
					pass

		# If this is first iteration, initialize open list
		if algoData.algoFields[0] == 0:
			tempOpen = []
			for i in range(len(algoData.tiles)):
				for j in range(len(algoData.tiles[i])):
					tempOpen.append([i, j])
			algoData.open = tempOpen

		# Remove neighbor coordinates that are in closed list
		for neighbor in neighbors:
			# print("Neighbor: ", neighbor)
			# print("Closed: ", algoData.closed)
			if neighbor in algoData.closed:
				neighbors.remove(neighbor)
		# print(neighbors)

		# Find neighbor with the least f val
		leastFCoord = None
		leastF = None
		leastStepCost = None
		for neighbor in neighbors:
			i = neighbor[0]
			j = neighbor[1]
			tempTile = algoData.tiles[i][j]

			# Set the temporary cost to move to temporary tile from current tile
			tempStepCost = None
			if tempTile.getType() is TileType.TREES_VERYLIGHT:
				tempStepCost = 100
			elif tempTile.getType() is TileType.TREES_LIGHT:
				tempStepCost = 150
			elif tempTile.getType() is TileType.TREES_MEDIUM:
				tempStepCost = 200
			elif tempTile.getType() is TileType.TREES_HEAVY:
				tempStepCost = 250
			elif tempTile.getType() is TileType.TREES_VERYHEAVY:
				tempStepCost = 300
			elif tempTile.getType() is TileType.ROCKS:
				tempStepCost = 1000
			elif tempTile.getType() is TileType.PATH:
				tempStepCost = 0

			# Set temporary g-val, h-val, and f-val
			tempG = tempStepCost + algoData.algoFields[0]
			tempH = (abs(i - 9) + abs(j - algoData.goalX)) * HEURISTIC_SCALAR
			tempF = tempG + tempH

			# If neighbor is PATH tile
			if tempTile.getType() is TileType.PATH:
				# If neighbor is goal tile set goal tile as leastFCoord
				if i == 9 and j == algoData.goalX:
					leastFCoord = neighbor
					leastF = tempF
					leastStepCost = tempStepCost
					continue
				# If neighbor is a previous laid path, ignore it and add to closed list
				else:
					algoData.closed.append(neighbor)
					# algoData.open.remove(neighbor)
					continue

			# If no coordinates stored yet or if tempF is less than leastF, store temporary coordinates and value
			if leastFCoord is None or tempF < leastF:
				leastFCoord = neighbor
				leastF = tempF
				leastStepCost = tempStepCost
			else:
				algoData.closed.append(neighbor)
				algoData.open.remove(neighbor)
		# print("Next Coord: ", leastFCoord)
		# print("")

		algoData.closed.append([algoData.currentY, algoData.currentX])
		# algoData.open.remove([algoData.currentY, algoData.currentX])

		# Update currentX and currentY
		algoData.currentX = leastFCoord[1]
		algoData.currentY = leastFCoord[0]

		# Update TileType to PATH
		algoData.tiles[algoData.currentY][algoData.currentX].setType(TileType.PATH)

		# Update guiTiles to visually show new PATH tile placement
		x = algoData.currentX
		y = algoData.currentY
		algoData.canvas.delete(algoData.guiTiles[y][x])
		x1 = algoData.currentX * 75
		y1 = algoData.currentY * 75
		x2 = x1 + 75
		y2 = y1 + 75
		algoData.guiTiles[y][x] = algoData.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PATH)
		algoData.canvas.tag_raise(startOutlineID)
		algoData.canvas.tag_raise(goalOutlineID)

		# Set g-val for current configuration
		oldG = algoData.algoFields[0]
		algoData.algoFields[0] = oldG + leastStepCost

		# Set h-val for current configuration
		algoData.algoFields[1] = (abs(algoData.currentY - 9) + abs(
			algoData.currentX - algoData.goalX)) * HEURISTIC_SCALAR

		# Set f-val for current configuration
		algoData.algoFields[2] = algoData.algoFields[0] + algoData.algoFields[1]

		g = algoData.algoFields[0]
		h = algoData.algoFields[1]
		f = algoData.algoFields[2]

		# Update g, h, and f GUI labels
		algoData.canvas.delete(algoData.rightHandElements[1])
		algoData.rightHandElements[1] = algoData.canvas.create_text(800, 200, anchor=NW, text="G: \t" + str(g), font=("Purisa", 12))

		algoData.canvas.delete(algoData.rightHandElements[2])
		algoData.rightHandElements[2] = algoData.canvas.create_text(800, 250, anchor=NW, text="H: \t" + str(h), font=("Purisa", 12))

		algoData.canvas.delete(algoData.rightHandElements[3])
		algoData.rightHandElements[3] = algoData.canvas.create_text(800, 300, anchor=NW, text="F: \t" + str(f), font=("Purisa", 12))

		coordString = str("[" + str(algoData.currentY) + ", " + str(algoData.currentX) + "]")
		print("Current Coord: ", coordString, "\n")


# Run driver program
if __name__ == "__main__":
	main()
