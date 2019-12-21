#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

import math


def main():
	""" finds how many asteroids each asteroid can see """
	grid = []
	with open('asteroid_belt.txt', 'r') as r:
		for line in r:
			grid.append([c for c in line.strip()])
	# need to swap grid because we read in x as y and y as x and I'm too lazy to read it in correctly
	grid = list(map(list, zip(*grid)))

	asteroids = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == '#':
				asteroids.append((i, j))

	best = 0, 0
	can_see = {}

	for asteroid in asteroids:
		lines_of_sight = {}
		for ast in asteroids:
			if ast != asteroid:
				rad = math.atan2((ast[0] - asteroid[0]), -(asteroid[1] - ast[1]))
				if rad < 0:
					rad = math.pi + abs(rad)
				d = dist_to(asteroid, ast)
				lines_of_sight.setdefault(rad, {})[d] = ast
		if len(lines_of_sight) > len(can_see):
			best = asteroid
			can_see = lines_of_sight

	print("{} sees {}".format(best, len(can_see)))

	blasted = 0
	sorted_lines = sorted(can_see.keys())
	if len(sorted_lines) > 200:
		sight = can_see[sorted_lines[199]]
		dists = sorted(sight.keys())
		print(sight[dists[0]])
	else:
		i = 0
		while blasted < 200:
			if sorted_lines[i] in can_see:
				sight = can_see[sorted_lines[i]]
				blasted += 1
				if blasted == 200:
					dists = sorted(sight.keys())
					print("final {} {}".format(sorted_lines[i], sight[dists[0]]))
				elif len(sight) == 1:
					del can_see[sorted_lines[i]]
				else:
					dists = sorted(sight.keys())
					del sight[dists[0]]
			i = (i + 1) % len(sorted_lines)
	return


def dist_to(fr, to):
	return math.sqrt(math.pow(abs(to[0]-fr[0]), 2) + math.pow(abs(to[1]-fr[1]), 2))


def test():
	p1 = (0, 0)
	points = [(0, 1),
			  (0, -1),
			  (1, 0),
			  (-1, 0)]
	# move x axis down 90 degrees
	#       y
	#       |   (2, 1) -> (1, -2) -> (-2, -1) -> (-1, 2)
	# -x _ _|_ _ x
	#       |
	#       |
	#       -y
	can_see = {}
	for p in points:
		rad = math.atan2((p[0] - p1[0]), p1[1] - p[1])
		if rad < 0:
			rad = math.pi + abs(rad)
		can_see[rad] = p
	sorted_lines = sorted(can_see.keys())
	for s in sorted_lines:
		print("{}: {}".format(can_see[s], s))
	return


if __name__ == "__main__":
	main()
