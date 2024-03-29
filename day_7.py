#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

from enum import Enum


class State(Enum):
	NEW = 1
	ACTIVE = 2
	PAUSED = 3
	FINISHED = 4


class IntCode:
	def __init__(self, values, identifier, phase):
		self.values = values
		self.index = 0
		self.identifier = identifier
		self.inputs = [phase]
		self.state = State.NEW
		self.last_out = -1

	def run(self, new_input):
		self.inputs.append(new_input)
		out = get_output(self.values, self.index, self.inputs)
		self.state = out[0]
		self.index = out[1]
		if self.state != State.FINISHED:
			self.last_out = out[2]
		return self.state, self.last_out


def get_op(value):
	return int(value % 100), int(value/100 % 10) == 1, int(value/1000 % 10) == 1


def get_params(values, f_mode, s_mode, i):
	f_val = values[i + 1] if f_mode else values[values[i + 1]]
	s_val = values[i + 2] if s_mode else values[values[i + 2]]
	return f_val, s_val


def get_output(values, i, inputs):
	while i < len(values):
		op = get_op(values[i])
		if op[0] == 1:
			params = get_params(values, op[1], op[2], i)
			values[values[i+3]] = params[0] + params[1]
			# print("{} + {} = {}".format(params[0], params[1], values[values[i+3]]))
			i += 4
		elif op[0] == 2:
			params = get_params(values, op[1], op[2], i)
			values[values[i+3]] = params[0] * params[1]
			i += 4
		elif op[0] == 3:
			if inputs:
				values[values[i+1]] = inputs.pop(0)
				i += 2
			else:
				return State.PAUSED, i, None
		elif op[0] == 4:
			return State.ACTIVE, i+2, values[values[i + 1]]
		elif op[0] == 5:
			params = get_params(values, op[1], op[2], i)
			if params[0] != 0:
				i = params[1]
			else:
				i += 3
		elif op[0] == 6:
			params = get_params(values, op[1], op[2], i)
			i = params[1] if params[0] == 0 else i + 3
		elif op[0] == 7:
			params = get_params(values, op[1], op[2], i)
			values[values[i+3]] = 1 if params[0] < params[1] else 0
			i += 4
		elif op[0] == 8:
			params = get_params(values, op[1], op[2], i)
			values[values[i+3]] = 1 if params[0] == params[1] else 0
			i += 4
		elif op[0] == 99:
			return State.FINISHED, i, None
		else:
			print("something went wrong")
			return None


def get_phases(lower, upper):
	phases = []
	for i in range(lower, upper):
		for j in range(lower, upper):
			for k in range(lower, upper):
				for h in range(lower, upper):
					for m in range(lower, upper):
						if i != j and i != k and i != h and i != m and j != k and j != h and j != m and k != h and k != m and h != m:
							phases.append([i, j, k, h, m])
	return phases


def main():
	# values = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
	# values = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
	values = [3,8,1001,8,10,8,105,1,0,0,21,46,67,76,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,4,9,9,102,3,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

	phases = get_phases(5, 10)
	max_thrust = 0, None
	for phase in phases:
		int_machines = [IntCode(list(values), 'A', phase[0]),
						IntCode(list(values), 'B', phase[1]),
						IntCode(list(values), 'C', phase[2]),
						IntCode(list(values), 'D', phase[3]),
						IntCode(list(values), 'E', phase[4])]

		i = 0
		state = None
		signal = 0

		# Go until one machine has finished, then proceed to machine E (until we come around to A again)
		while state != State.FINISHED or i > 0:
			cur_state, signal = int_machines[i].run(signal)
			# keep first FINISHED state
			if state != State.FINISHED:
				state = cur_state
			i = (i + 1) % len(int_machines)

		if signal > max_thrust[0]:
			max_thrust = signal, phase
	print(max_thrust)


if __name__ == "__main__":
	main()
