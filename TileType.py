# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: PROJECT
# Due Date: December 2, 2019
# Signature: Jason James
# Score: _________________

from enum import Enum


# Class acts as an Enum to hold the finite amount of different TileTypes
class TileType(Enum):
	PATH = 0
	TREES_VERYLIGHT = 1
	TREES_LIGHT = 2
	TREES_MEDIUM = 3
	TREES_HEAVY = 4
	TREES_VERYHEAVY = 5
	ROCKS = 6
