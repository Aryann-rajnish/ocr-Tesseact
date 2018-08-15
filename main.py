import sys
import os
from subprocess import call
import argparse

IMG = [".jpg",".gif",".png",".tga",".tif",".bmp"]
F = open(os.devnull, 'w')

class ArgMisException(Exception):
	def __init__(self):
		print("usage: {} <dirname>".format(sys.argv[0]))
		sys.exit(1)

def create_directory(path):
	if not os.path.exists(path):
	    os.makedirs(path)

def check_path(path):
	return bool(os.path.exists(path))

def main(input_path, output_path):
	if call(['which', 'tesseract']):
		print("you have not installed tesseract-ocr, use sudo apt-get install tesseract-ocr to resolve")
	elif check_path(input_path):

		count = 0
		files = 0

		for f in os.listdir(input_path):
			ext = os.path.splitext(f)[1]

			if ext.lower() not in IMG:
				files += 1
				continue
			else :

				if count == 0:
					create_directory(output_path)
				count += 1
				image_file_name = os.path.join(input_path, f)
				filename = os.path.splitext(f)[0]
				filename = ''.join(e for e in filename if e.isalnum() or e == '-')
				text_file_path = os.path.join(output_path, filename)

				call(["tesseract", image_file_name, text_file_path], stdout=F)

				print(str(count) + (" file" if count == 1 else " files") + " completed")

		if count + files == 0:
			print("No files found at your given location")
		else :
			print(str(count) + " / " + str(count + files) + " files converted")
	else :
		print("No directory found at " + format(input_path))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("input_dir")
	parser.add_argument('output_dir', nargs='?')
	args = parser.parse_args()
	input_path = os.path.abspath(args.input_dir)
	if args.output_dir:
		output_path = os.path.abspath(args.output_dir)
	else:
		output_path = os.path.join(input_path,'output')
	main(input_path, output_path)
