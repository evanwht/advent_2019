#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

import math
from functools import reduce    # need this line if you're using Python3.x


class Moon:
	def __init__(self, x, y, z):
		self.og_x, self.og_y, self.og_z = x, y, z
		self.x, self.y, self.z = x, y, z
		self.vel_x, self.vel_y, self.vel_z = 0, 0, 0

	def accelerate(self, others):
		# first modify velocity by each of the other moons
		for o in others:
			if o is not self:
				if o.x != self.x:
					self.vel_x = self.vel_x + (1 if o.x > self.x else -1)
				if o.y != self.y:
					self.vel_y = self.vel_y + (1 if o.y > self.y else -1)
				if o.z != self.z:
					self.vel_z = self.vel_z + (1 if o.z > self.z else -1)

	def move(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.z += self.vel_z

	def reset(self):
		self.x, self.y, self.z = self.og_x, self.og_y, self.og_z
		self.vel_x, self.vel_y, self.vel_z = 0, 0, 0

	def energy(self):
		return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z))

	def has_returned(self, dimension):
		if dimension == 'x':
			return self.x == self.og_x and self.vel_x == 0
		elif dimension == 'y':
			return self.y == self.og_y and self.vel_y == 0
		elif dimension == 'z':
			return self.z == self.og_z and self.vel_z == 0

	def __repr__(self):
		return '{' + "{}, {}, {}".format(self.x, self.y, self.z) + '}'


def main():
	io = Moon(16, -8, 13)
	europa = Moon(4, 10, 10)
	ganymede = Moon(17, -5, 6)
	callisto = Moon(13, -3, 0)

	moons = [io, europa, ganymede, callisto]

	for i in range(1000):
		for moon in moons:
			moon.accelerate(moons)
		for moon in moons:
			moon.move()
	print(sum([moon.energy() for moon in moons]))

	for moon in moons:
		moon.reset()

	# find the cycles of x, y, and z dimensions for each pair
	x, y, z, i = 0, 0, 0, 0
	while x == 0 or y == 0 or z == 0:
		i += 1
		for moon in moons:
			moon.accelerate(moons)
		for moon in moons:
			moon.move()
		if all([moon.has_returned('x') for moon in moons]):
			x = i
		if all([moon.has_returned('y') for moon in moons]):
			y = i
		if all([moon.has_returned('z') for moon in moons]):
			z = i

	print("{} {} {}".format(x, y, z))
	print(lcm([x, y, z]))
	return


def lcm(denominators):
	return reduce(lambda a, b: a*b // math.gcd(a, b), denominators)


if __name__ == "__main__":
	main()
