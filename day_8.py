#!/usr/bin/env python
__author__ = "evanwht1@gmail.com"


def main():
	picture = {}
	digits = ''
	with open('picture_data_day_8.txt', 'r') as r:
		digits = r.readline()

	layer = 0
	column = 0
	row = 0
	for digit in digits:
		l = picture.setdefault(layer, {}).setdefault(row, {})[column] = int(digit)
		column = (column + 1) % 25
		row = (row + 1) % 6 if column == 0 else row
		layer = layer + 1 if column == 0 and row == 0 else layer 

	least_0_count = -1, -1
	for n, l in picture.items():
		count = 0
		for r, c in l.items():
			for k, v in c.items():
				if v == 0:
					count += 1
		if least_0_count[0] == -1 or count < least_0_count[0]:
			least_0_count = count, n

	print(least_0_count)

	num_1_digits = 0
	num_2_digits = 0
	for r,c in picture[least_0_count[1]].items():
		for k,v in c.items():
			if v == 1:
				num_1_digits += 1
			elif v == 2:
				num_2_digits += 1
	print(num_2_digits * num_1_digits)

	final_pic = [[-1 for j in range(len(picture[0][0]))] for i in range(len(picture[0]))]
	for n,l in picture.items():
		for r,c in l.items():
			for k,v in c.items():
				if v != 2 and final_pic[r][k] == -1:
					final_pic[r][k] = v
	for r in final_pic:
		print(str(r).replace('[', '').replace(']', '').replace(',', '').replace('0', ' ').replace('1',  u"\u2588"))

	return


if __name__ == "__main__":
	main()
