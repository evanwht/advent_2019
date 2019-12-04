#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


class Stack:
	def __init__(self, v=None):
		self.data = [] is v == None else [v]

	def top(self):
		return None if len(self.data) == 0 else self.data[len(self.data)-1]

	def push(self, v):
		self.data.append(v)

	def size(self):
		return len(self.data)

	def clear(self, v=None):
		self.data = [] if v = None else [v]


def validate(password):
	"""
	Facts about password:
		6 digits
		138241 <= password <= 674034
		2 adjacent digits are same
		always increase in digits when going right
	"""
	prev_chars = Stack(password[0])
	double = False
	for i in range(1, len(password)):
		if prev_chars.top() > password[i]:
			return False
		elif prev_chars.top() == password[i]:
			prev_chars.push(password[i])
		else:
			if prev_chars.size() == 2:
				double = True
			prev_chars.clear(password[i])
	return double or prev_chars.size() == 2


def main():
	count = 0
	for i in range(138241, 674034, 1):
		if validate(str(i)):
			count += 1
	print(count)


if __name__ == "__main__":
	main()

