#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

import math
import sys


def get_output(values):
	for i in range(0, len(values), 4):
		op = values[i]
		if op == 1:
			values[values[i + 3]] = values[values[i + 1]] + values[values[i + 2]]
		elif op == 2:
			values[values[i + 3]] = values[values[i + 1]] * values[values[i + 2]]
		elif op == 99:
			return values[0]
		else:
			print("something went wrong")
			return None
	return None


def main():
	data = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19, 1, 6, 19, 23, 2, 23, 6, 27, 1, 5, 27, 31, 1,
			31, 9, 35, 2, 10, 35, 39, 1, 5, 39, 43, 2, 43, 10, 47, 1, 47, 6, 51, 2, 51, 6, 55, 2, 55, 13, 59, 2, 6, 59,
			63, 1, 63, 5, 67, 1, 6, 67, 71, 2, 71, 9, 75, 1, 6, 75, 79, 2, 13, 79, 83, 1, 9, 83, 87, 1, 87, 13, 91, 2,
			91, 10, 95, 1, 6, 95, 99, 1, 99, 13, 103, 1, 13, 103, 107, 2, 107, 10, 111, 1, 9, 111, 115, 1, 115, 10, 119,
			1, 5, 119, 123, 1, 6, 123, 127, 1, 10, 127, 131, 1, 2, 131, 135, 1, 135, 10, 0, 99, 2, 14, 0, 0]

	data[1] = 12
	data[2] = 2

	# answer to challenge 1
	ans = get_output(list(data))
	print(ans)

	desired_value = 19690720

	for i in range(0, 100):
		for j in range(0, 100):
			new_data = list(data)
			new_data[1] = i
			new_data[2] = j
			if get_output(new_data) == desired_value:
				print("{}_{}".format(i, j))


if __name__ == "__main__":
	main()
