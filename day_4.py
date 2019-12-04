#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


def validate(password):
	"""
	Facts about password:
		6 digits
		138241 <= password <= 674034
		2 adjacent digits are same
		always increase in digits when going right
	"""
	double = False
	for i in range(len(password)-1):
		if password[i] > password[i+1]:
			return False
		if password[i] == password[i+1]:
			double = True
	return double


def main():
	count = 0
	for i in range(138241, 674034, 1):
		if validate(str(i)):
			count += 1
	print(count)
	return


if __name__ == "__main__":
	main()