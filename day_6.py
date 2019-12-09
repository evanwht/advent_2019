#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


def main():
	orbits = {}
	with open('day_6_orbits.txt', 'r') as r:
		for orbit in r:
			i = orbit.find(')')
			center = orbit[:i].strip()
			orb = orbit[i+1:].strip()
			if center not in orbits:
				orbits[center] = []
			orbits[center].append(orb)
	cen = find_a_center(orbits)
	num = count(cen, orbits, 0)
	while orbits:
		cen = find_a_center(orbits)
		num += count(cen, orbits, 0)
	print(num)


def find_a_center(system):
	for i in system:
		is_center = True
		for j in system:
			if i in system[j]:
				is_center = False
		if is_center:
			return i
	return None


def count(planet, orbits, depth):
	if planet in orbits:
		return sum([count(i, orbits, depth + 1) for i in orbits.pop(planet)]) + depth
	return depth


if __name__ == "__main__":
	main()

