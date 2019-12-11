#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"

from enum import Enum


class State(Enum):
	ACTIVE = 1
	PAUSED = 2
	FINISHED = 3

	def __repr__(self):
		return self.name


class Mode(Enum):
	POS = 0
	VAL = 1
	REL = 2

	def __repr__(self):
		return self.__str__()


class Op:
	def __init__(self, value):
		self.op = int(value % 100)
		self.f_mode, self.s_mode, self.t_mode = None, None, None
		if self.op < 99:
			self.f_mode = Mode(int(value / 100 % 10))
		if self.op in [1, 2, 5, 6, 7, 8]:
			self.s_mode = Mode(int(value / 1000 % 10))
		if self.op in [1, 2, 8, 7]:
			self.t_mode = Mode(int(value / 10000 % 10))

	def __str__(self):
		return '{' + "{}, {}, {}".format(self.op, self.f_mode, self.s_mode) + '}'


class Output:
	def __init__(self, state, index, offset, val=None):
		self.state = state
		self.index = index
		self.offset = offset
		self.val = val


	def __str__(self):
		return '{' + "{}, {}, {}, {}".format(self.state, self.index, self.offset, self.val) + '}'


class IntCode:
	def __init__(self, values, identifier):
		self.values = [0 for i in range(len(values) * 110)]
		self.values[0:len(values)] = values[:]
		self.identifier = identifier
		self.inputs = []
		self.last_out = Output(None, 0, 0)

	def input(self, value):
		self.inputs.append(value)

	def run(self):
		out = get_output(self.values, self.last_out.index, self.last_out.offset, self.inputs)
		if out.state == State.FINISHED:
			out.val = self.last_out.val
		self.last_out = out
		return self.last_out


def get_params(values, i, offset, f_mode, s_mode=None, t_mode=None):
	f_val, s_val, t_val = None, None, None
	if f_mode is not None:
		if f_mode == Mode.VAL:
			f_val = values[i + 1]
		elif f_mode == Mode.POS:
			f_val = values[values[i + 1]]
		else:
			f_val = values[offset + values[i + 1]]
	if s_mode is not None:
		if s_mode == Mode.VAL:
			s_val = values[i + 2]
		elif s_mode == Mode.POS:
			s_val = values[values[i + 2]]
		else:
			s_val = values[offset + values[i + 2]]
	if t_mode is not None:
		if t_mode == Mode.VAL:
			t_val = values[i + 3]
		elif t_mode == Mode.POS:
			t_val = values[values[i + 3]]
		else:
			t_val = values[offset + values[i + 3]]
	return f_val, s_val, t_val


def get_output(values, i, offset, inputs):
	while i < len(values):
		op = Op(values[i])
		if op.op == 1:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			values[values[i + 3] + (offset if op.t_mode == Mode.REL else 0)] = params[0] + params[1]
			i += 4
		elif op.op == 2:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			values[values[i + 3] + (offset if op.t_mode == Mode.REL else 0)] = params[0] * params[1]
			i += 4
		elif op.op == 3:
			if inputs:
				values[values[i + 1] + (offset if op.f_mode == Mode.REL else 0)] = inputs.pop(0)
				i += 2
			else:
				return Output(State.PAUSED, i, offset)
		elif op.op == 4:
			params = get_params(values, i, offset, op.f_mode)
			return Output(State.ACTIVE, i + 2, offset, params[0])
		elif op.op == 5:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			if params[0] != 0:
				i = params[1]
			else:
				i += 3
		elif op.op == 6:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			i = params[1] if params[0] == 0 else i + 3
		elif op.op == 7:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			values[values[i + 3] + (offset if op.t_mode == Mode.REL else 0)] = 1 if params[0] < params[1] else 0
			i += 4
		elif op.op == 8:
			params = get_params(values, i, offset, op.f_mode, op.s_mode)
			values[values[i + 3] + (offset if op.t_mode == Mode.REL else 0)] = 1 if params[0] == params[1] else 0
			i += 4
		elif op.op == 9:
			params = get_params(values, i, offset, op.f_mode)
			offset += params[0]
			i += 2
		elif op.op == 99:
			return Output(State.FINISHED, i, offset)
		else:
			print("something went wrong")
			return None


def main():
	# values = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
	# values = [1102,34915192,34915192,7,4,7,99,0]
	# values = [104,1125899906842624,99]
	values = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,0,1020,1101,34,0,1004,1101,0,26,1008,1102,1,37,1011,1101,39,0,1018,1102,587,1,1022,1101,1,0,1021,1102,22,1,1012,1101,0,33,1014,1101,24,0,1016,1101,0,752,1029,1101,36,0,1002,1101,35,0,1006,1101,32,0,1009,1102,38,1,1003,1102,584,1,1023,1101,0,20,1001,1102,892,1,1025,1102,29,1,1000,1101,411,0,1026,1102,1,901,1024,1101,0,761,1028,1101,23,0,1017,1102,30,1,1013,1101,0,27,1015,1102,28,1,1005,1101,408,0,1027,1101,25,0,1007,1102,31,1,1019,1101,0,21,1010,109,5,1207,-2,39,63,1005,63,199,4,187,1105,1,203,1001,64,1,64,1002,64,2,64,109,12,21102,40,1,-1,1008,1016,40,63,1005,63,229,4,209,1001,64,1,64,1106,0,229,1002,64,2,64,109,-5,1207,-5,24,63,1005,63,249,1001,64,1,64,1106,0,251,4,235,1002,64,2,64,109,-14,2102,1,6,63,1008,63,32,63,1005,63,271,1106,0,277,4,257,1001,64,1,64,1002,64,2,64,109,2,1202,1,1,63,1008,63,20,63,1005,63,303,4,283,1001,64,1,64,1106,0,303,1002,64,2,64,109,7,2108,34,2,63,1005,63,319,1106,0,325,4,309,1001,64,1,64,1002,64,2,64,109,6,2101,0,-6,63,1008,63,24,63,1005,63,349,1001,64,1,64,1105,1,351,4,331,1002,64,2,64,109,4,21107,41,42,0,1005,1017,369,4,357,1105,1,373,1001,64,1,64,1002,64,2,64,109,5,21101,42,0,-5,1008,1017,41,63,1005,63,397,1001,64,1,64,1106,0,399,4,379,1002,64,2,64,109,9,2106,0,-4,1106,0,417,4,405,1001,64,1,64,1002,64,2,64,109,-20,21108,43,43,0,1005,1011,435,4,423,1105,1,439,1001,64,1,64,1002,64,2,64,109,-15,2102,1,8,63,1008,63,34,63,1005,63,465,4,445,1001,64,1,64,1105,1,465,1002,64,2,64,109,3,1201,6,0,63,1008,63,28,63,1005,63,491,4,471,1001,64,1,64,1106,0,491,1002,64,2,64,109,18,21108,44,46,0,1005,1017,511,1001,64,1,64,1106,0,513,4,497,1002,64,2,64,109,12,1205,-8,527,4,519,1105,1,531,1001,64,1,64,1002,64,2,64,109,-17,1208,-3,32,63,1005,63,553,4,537,1001,64,1,64,1105,1,553,1002,64,2,64,109,-13,1208,10,31,63,1005,63,573,1001,64,1,64,1105,1,575,4,559,1002,64,2,64,109,17,2105,1,7,1105,1,593,4,581,1001,64,1,64,1002,64,2,64,109,-8,2107,19,-7,63,1005,63,615,4,599,1001,64,1,64,1105,1,615,1002,64,2,64,109,4,1206,8,629,4,621,1106,0,633,1001,64,1,64,1002,64,2,64,109,-2,2101,0,-6,63,1008,63,34,63,1005,63,655,4,639,1105,1,659,1001,64,1,64,1002,64,2,64,109,10,1205,0,671,1105,1,677,4,665,1001,64,1,64,1002,64,2,64,109,-21,2107,26,8,63,1005,63,693,1106,0,699,4,683,1001,64,1,64,1002,64,2,64,109,19,1201,-9,0,63,1008,63,30,63,1005,63,719,1105,1,725,4,705,1001,64,1,64,1002,64,2,64,109,9,1206,-6,741,1001,64,1,64,1106,0,743,4,731,1002,64,2,64,109,-5,2106,0,6,4,749,1001,64,1,64,1105,1,761,1002,64,2,64,109,-14,1202,-1,1,63,1008,63,27,63,1005,63,781,1105,1,787,4,767,1001,64,1,64,1002,64,2,64,109,1,21107,45,44,5,1005,1014,807,1001,64,1,64,1105,1,809,4,793,1002,64,2,64,109,8,21101,46,0,0,1008,1017,46,63,1005,63,835,4,815,1001,64,1,64,1106,0,835,1002,64,2,64,109,-26,2108,20,10,63,1005,63,857,4,841,1001,64,1,64,1106,0,857,1002,64,2,64,109,24,21102,47,1,-5,1008,1010,46,63,1005,63,881,1001,64,1,64,1106,0,883,4,863,1002,64,2,64,109,6,2105,1,3,4,889,1001,64,1,64,1105,1,901,4,64,99,21102,27,1,1,21101,915,0,0,1105,1,922,21201,1,29830,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21102,1,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,21201,-2,0,-2,109,-3,2106,0,0]
	machine = IntCode(values, 'A')
	machine.input(1)
	state = None
	outputs = []
	while state != State.FINISHED:
		out = machine.run()
		state = out.state
		if state != State.FINISHED:
			outputs.append(out.val)
	print(outputs)
	return


if __name__ == "__main__":
	main()
