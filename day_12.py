#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


class Moon:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vel_x = 0
		self.vel_y = 0
		self.vel_z = 0

	def accelerate(self, others):
		# first modify velocity by each of the other moons
		for o in others:
			if o.x != self.x:
				self.vel_x = self.vel_x + (1 if o.x > self.x else -1)
			if o.y != self.y:
				self.vel_y= self.vel_y + (1 if o.y > self.y else -1)
			if o.z != self.z:
				self.vel_z = self.vel_z + (1 if o.z > self.z else -1)

	def move(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.z += self.vel_z

	def energy(self):
		return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z))


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
	return


if __name__ == "__main__":
	main()
