#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

import sys
import math


def main():
	""" finds how many asteroids each asteroid can see """
	grid = []
	with open('asteroid_belt.txt', 'r') as r:
		for line in r:
			grid.append([c for c in line.strip()])
	# need to swap grid because we read in x as y and y as x
	grid = list(map(list, zip(*grid)))

	steps = get_steps(grid)

	best = 0, 0
	num_seen = 0

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pos = (i, j)
			sees = 0
			if grid[pos[0]][pos[1]] == '#':
				for step in steps:
					sees += num_see(grid, pos, step[0], step[1])
				if sees > num_seen:
					num_seen = sees
					best = pos

	print("{} sees {}".format(best, num_seen))

	# start blasting asteroids
	nth = find_nth_blasted(grid, best, steps, 200)
	print(nth)
	return


def comparator_qaud(pos):
	return math.atan2(pos[1], pos[0])


def walk(grid, pos, x, y):
	pos = (pos[0] + x, pos[1] + y)
	while in_bounds(pos[0], len(grid)) and in_bounds(pos[1], len(grid[0])) and grid[pos[0]][pos[1]] == '.':
		pos = (pos[0]+x, pos[1]+y)
	if in_bounds(pos[0], len(grid)) and in_bounds(pos[1], len(grid[0])) and grid[pos[0]][pos[1]] == '#':
		return pos
	return None


def find_nth_blasted(grid, start, steps, n):
	# start by looking 'up'
	steps.sort(key=comparator_qaud)
	# remove this as it will move along the axis in the next quadrant
	steps.remove((0, 1))
	print(steps)

	# quadrant 1
	blasted = 0
	for step in steps:
		pos = walk(grid, start, step[1], -step[0])
		if pos:
			grid[pos[0]][pos[1]] = '.'
			blasted += 1
			if blasted == n:
				return pos
	# quadrant 2
	for step in steps:
		pos = walk(grid, start, step[0], step[1])
		if pos:
			grid[pos[0]][pos[1]] = '.'
			blasted += 1
			if blasted == n:
				return pos
	# quadrant 3
	for step in steps:
		pos = walk(grid, start, -step[1], step[0])
		if pos:
			grid[pos[0]][pos[1]] = '.'
			blasted += 1
			if blasted == n:
				return pos
	# quadrant 4
	for step in steps:
		pos = walk(grid, start, -step[0], -step[1])
		if pos:
			grid[pos[0]][pos[1]] = '.'
			blasted += 1
			if blasted == n:
				return pos
	return None


def get_steps(grid):
	steps = []
	for k in range(1, len(grid)):
		for l in range(1, len(grid[0])):
			if k != l:
				sub_steps = [((k % i[0] == 0 and l % i[1] == 0 and (k/i[0] == l/i[1])) and (k != i[0] and l != i[1])) for i in steps]
				# print("{} -> {}".format((k, l), [j for j in steps if sub_steps[steps.index(j)]]))
				if not any(sub_steps):
					steps.append((k, l))
	steps.extend([(0, 1), (1, 0), (1, 1)])
	return steps


def num_see(grid, pos, x, y):
	"""
	Determines how many other asteroids this asteroid as position pos can see with the given x and y steps.
	E.G. if the x and y steps are both 1, this will determine if there are any asteroids in sight when moving
	forward 1 in both x and y, forward 1 in x and backward 1 in y, backward 1 in x and forward 1
	in y, and finally backward 1 in both x and y.
	Return value is always between 0 and 4, as there are only 4 directions you can go with each set of x and y steps

	Returns 0 if the x or y steps are divisible by 2 (might be asteroid closer in and therefor should have been called
	by the smaller steps)
	"""
	num = 0

	# both forward
	cur_x, cur_y = (pos[0] + x), (pos[1] + y)
	seen = False
	while seen is False and in_bounds(cur_x, len(grid)) and in_bounds(cur_y, len(grid[0])):
		seen = True if grid[cur_x][cur_y] == '#' else False
		cur_x += x
		cur_y += y
	num += 1 if seen else 0

	# x back, y forward
	if x > 0 and y > 0:
		cur_x, cur_y = (pos[0] - x), (pos[1] + y)
		seen = False
		while seen is False and in_bounds(cur_x, len(grid)) and in_bounds(cur_y, len(grid[0])):
			seen = True if grid[cur_x][cur_y] == '#' else False
			cur_x -= x
			cur_y += y
		num += 1 if seen else 0

	# both back
	cur_x, cur_y = (pos[0] - x), (pos[1] - y)
	seen = False
	while seen is False and in_bounds(cur_x, len(grid)) and in_bounds(cur_y, len(grid[0])):
		seen = True if grid[cur_x][cur_y] == '#' else False
		cur_x -= x
		cur_y -= y
	num += 1 if seen else 0

	# x forward, y back
	if x > 0 and y > 0:
		cur_x, cur_y = (pos[0] + x), (pos[1] - y)
		seen = False
		while seen is False and in_bounds(cur_x, len(grid)) and in_bounds(cur_y, len(grid[0])):
			seen = True if grid[cur_x][cur_y] == '#' else False
			cur_x += x
			cur_y -= y
		num += 1 if seen else 0

	return num


def in_bounds(pos, upper):
	return -1 < pos < upper


def create_grid(x, y):
	return [['' for j in range(y)] for i in range(x)]


def tests():
	# expected = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 3), (2, 5), (3, 1), (3, 2), (3, 4), (3, 5), (4, 1), (4, 3), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4), (0, 1), (1, 0), (1, 1)]
	# if get_steps(create_grid(6, 6)) != expected:
	# 	print("get_steps not working correctly")
	# 	sys.exit(1)

	grid = [['#', '#', '#'],
			['#', '#', '#'],
			['#', '#', '#']]
	pos = find_nth_blasted(grid, (0, 0), get_steps(grid), 2)
	print(pos)


if __name__ == "__main__":
	main()
	# tests()
