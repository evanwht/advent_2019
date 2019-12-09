#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

from enum import Enum


class State(Enum):
	ACTIVE = 1
	PAUSED = 2
	STOPPED = 3


class IntCode:
	def __init__(self, values, phase):
		self.values = values
		self.index = 0
		self.inputs = [phase, 0]

	def input(self, value):
		self.inputs.append(value)

	def run(self):
		out = get_output(self.values, self.index, self.inputs)
		self.index = out[1]
		self.inputs = out[2]
		return out


def get_output(values, i, inputs):
	while i < len(values):
		op = values[i] % 100
		if op == 1:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i+1] if first else values[values[i+1]]
			s_val = values[i+2] if second else values[values[i+2]]
			values[values[i+3]] = f_val + s_val
			i += 4
		elif op == 2:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i+1] if first else values[values[i+1]]
			s_val = values[i+2] if second else values[values[i+2]]
			values[values[i+3]] = f_val * s_val
			i += 4
		elif op == 3:
			if inputs:
				values[values[i+1]] = inputs.pop(0)
				i += 2
			else:
				return State.PAUSED, i, None
		elif op == 4:
			return State.ACTIVE, i, values[values[i+1]]
		elif op == 5:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i + 1] if first else values[values[i + 1]]
			s_val = values[i + 2] if second else values[values[i + 2]]
			if f_val != 0:
				i = s_val
			else:
				i += 3
		elif op == 6:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i + 1] if first else values[values[i + 1]]
			s_val = values[i + 2] if second else values[values[i + 2]]
			if f_val == 0:
				i = s_val
			else:
				i += 3
		elif op == 7:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i + 1] if first else values[values[i + 1]]
			s_val = values[i + 2] if second else values[values[i + 2]]
			values[values[i+3]] = 1 if f_val < s_val else 0
			i += 4
		elif op == 8:
			first = values[i] / 100 % 10 > 1
			second = values[i] / 1000 % 10 > 1
			f_val = values[i + 1] if first else values[values[i + 1]]
			s_val = values[i + 2] if second else values[values[i + 2]]
			values[values[i+3]] = 1 if f_val == s_val else 0
			i += 4
		elif op == 99:
			return State.STOPPED, i, values[0]
		else:
			print("something went wrong")
			return None
	return None


def main():
	values = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
	# values = [3,8,1001,8,10,8,105,1,0,0,21,46,67,76,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,4,9,9,102,3,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

	phases = []
	for i in range(5, 10):
		for j in range(5, 10):
			for k in range(5, 10):
				for h in range(5, 10):
					for m in range(5, 10):
						if i != j and i != k and i != h and i != m and j != k and j != h and j != m and k != h and k != m and h != m:
							phases.append([i, j, k, h, m])
	maxi = 0
	out = 0
	for phase in phases:
		while out is not None:
			for i in range(5):
				out = get_output(list(values), [phase[i], out])
			if out > maxi:
				maxi = out
	print(maxi)


if __name__ == "__main__":
	main()
