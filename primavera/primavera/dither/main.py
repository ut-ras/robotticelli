import base64
import argparse

from binascii import a2b_base64
from primavera.primavera.primavera import primavera
from venus.venus.venus import venus
from random import randint

encoder = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_";

def generate_key(n):
	key = ""
	for i in range(n): 
		key = key + encoder.substring[randint(0,65)]
	return key

def main():
	parser = argparse.ArgumentParser('main')
	parser.add_argument('-i', '--image', required=True)
	parser.add_argument('-p', '--palette-size', type=int, default=5)
	parser.add_argument('-c', '--colors', type=str, default = "primavera/montana.json")
	parser.add_argument('-d', '--dither', type=str)

	parser.add_argument('-r', '--resize', type=float, default=1)
	parser.add_argument('-o', '--overshoot', type=int, default=1)
	parser.add_argument('-m', '--merge',  action="store_true")
	parser.add_argument('-q', '--quick',  action="store_true")
	parser.add_argument('-e', '--entire', action="store_true")

	args = parser.parse_args()

	if args.image:
		print args.palette_size

		primavera(image=args.image, palette_size=args.palette_size, save_image="image.png",
		          save_labels="labels.npy", colors=args.colors, dither=args.dither, 
		          resize=args.resize, overshoot=args.overshoot, merge=args.merge,
        		  quick=args.quick, entire=args.entire)

		print "file processed through primavera, sending to venus"

		venus(labels="labels.npy",slots=4,pixels=400,write="out.txt")


if __name__ == '__main__':
	main()

