#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

import math


def fuel_to_launch(module):
	return math.floor(module / 3) - 2


def fuel_to_launch_fuel(fuel):
	extra_fuel = fuel_to_launch(fuel)
	total = 0
	while extra_fuel > 0:
		total += extra_fuel
		extra_fuel = fuel_to_launch(extra_fuel)
	return total


def main():
	modules = [94735, 80130, 127915, 145427, 89149, 91232, 100629, 97340, 86278, 87034, 147351, 123045, 91885, 85973, 64130,
			   113244, 58968, 76296, 127931, 98145, 120731, 98289, 110340, 118285, 60112, 57177, 58791, 59012, 66950,
			   139387, 145378, 86204, 147082, 84956, 134161, 148664, 74278, 96746, 144525, 81214, 70966, 107050, 134179,
			   138587, 80236, 139871, 104439, 64643, 145453, 94791, 51690, 94189, 148476, 79956, 81760, 149796, 109544,
			   57533, 142999, 126419, 115434, 57092, 64244, 109663, 94701, 109265, 145851, 95183, 84433, 53818, 106234,
			   127380, 149774, 59601, 138851, 54488, 100877, 136952, 61538, 67705, 60299, 130769, 113176, 106723, 133280,
			   111065, 63688, 139307, 122703, 60162, 89567, 63994, 66608, 126376, 136052, 112255, 98525, 134023, 141479,
			   98200]

	fuels = [fuel_to_launch(i) for i in modules]

	# answer to first challenge
	print(sum(fuels))

	extra_fuels = [fuel_to_launch_fuel(i) for i in fuels]

	# answer to second challenge
	print(sum(extra_fuels) + sum(fuels))


if __name__ == '__main__':
	main()

