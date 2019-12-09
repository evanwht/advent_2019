#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


def challenge_1():
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


def challenge_2():
	planets = {}
	with open('day_6_orbits.txt', 'r') as r:
		for orbit in r:
			i = orbit.find(')')
			center = orbit[:i].strip()
			orb = orbit[i + 1:].strip()
			if orb not in planets:
				planets[orb] = [center]
			else:
				planets[orb].append(center)
			if center not in planets:
				planets[center] = [orb]
			else:
				planets[center].append(orb)
	print(dist_to("YOU", "SAN", planets, []) - 1)


def dist_to(cur, end, planets, visited):
	visited.append(cur)
	if end in planets[cur]:
		return 0
	else:
		dists = [dist_to(i, end, planets, visited) for i in planets[cur] if i not in visited]
		t = -1 if not dists else max(dists)
		return 1 + t if t >= 0 else t


if __name__ == "__main__":
	challenge_2()

