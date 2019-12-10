#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


from enum import Enum


class State(Enum):
	ACTIVE = 1
	PAUSED = 2
	FINISHED = 3


class Mode(Enum):
	VAL = 0
	POS = 1
	REL = 2


class IntCode:
	def __init__(self, values, identifier, phase):
		self.values = values
		self.index = 0
		self.identifier = identifier
		self.inputs = [phase]
		self.state = None
		self.last_out = -1
		self.offset = 0

	def run(self, new_input):
		self.inputs.append(new_input)
		out = get_output(self.values, self.index, self.offset, self.inputs)
		self.state = out[0]
		self.index = out[1]
		self.offset = out[2]
		if self.state != State.FINISHED:
			self.last_out = out[3]
		return self.state, self.last_out


def get_op(value):
	return int(value % 100), Mode(int(value/100 % 10)), Mode(int(value/1000 % 10))


def get_params(values, offset, f_mode, s_mode, i):
	if f_mode == Mode.VAL:
		f_val = values[i+1]
	elif f_mode == Mode.POS:
		f_val = values[values[i + 1]]
	else:
		f_val = values[offset + values[i+2]]
	if s_mode == Mode.VAL:
		s_val = values[i+2]
	elif s_mode == Mode.POS:
		s_val = values[values[i + 2]]
	else:
		s_val = values[offset + values[i+2]]
	return f_val, s_val


def get_output(values, i, offset, inputs):
	while i < len(values):
		op = get_op(values[i])
		if op[0] == 1:
			params = get_params(values, offset, op[1], op[2], i)
			values[values[i+3]] = params[0] + params[1]
			# print("{} + {} = {}".format(params[0], params[1], values[values[i+3]]))
			i += 4
		elif op[0] == 2:
			params = get_params(values, offset, op[1], op[2], i)
			values[values[i+3]] = params[0] * params[1]
			i += 4
		elif op[0] == 3:
			if inputs:
				values[values[i+1]] = inputs.pop(0)
				i += 2
			else:
				return State.PAUSED, i, offset, None
		elif op[0] == 4:
			return State.ACTIVE, i+2, offset, values[values[i + 1]]
		elif op[0] == 5:
			params = get_params(values, offset, op[1], op[2], i)
			if params[0] != 0:
				i = params[1]
			else:
				i += 3
		elif op[0] == 6:
			params = get_params(values, offset, op[1], op[2], i)
			i = params[1] if params[0] == 0 else i + 3
		elif op[0] == 7:
			params = get_params(values, offset, op[1], op[2], i)
			values[values[i+3]] = 1 if params[0] < params[1] else 0
			i += 4
		elif op[0] == 8:
			params = get_params(values, offset, op[1], op[2], i)
			values[values[i+3]] = 1 if params[0] == params[1] else 0
			i += 4
		elif op[0] == 9:
			params = get_params(values, offset, op[1], op[2], i)
			offset += params[0]
			i += 2
		elif op[0] == 99:
			return State.FINISHED, i, offset, None
		else:
			print("something went wrong")
			return None



def main():
	return


if __name__ == "__main__":
	main()
