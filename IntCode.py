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


class IntCodeMachine:
	def __init__(self, values, identifier='', mult=1):
		self.values = [0 for i in range(len(values) * mult)]
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

	def state(self):
		return self.last_out.state


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
