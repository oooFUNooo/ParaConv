import os
import re
import argparse


def analyze(path, file, out, encord, args):

	text = open(path + '/' + file, 'r', encoding = encord)

	# Analyze
	for line in text:

		# Remove Line Feed
		line = line.rstrip('\n')

		# For Debug Purpose
		if args.line:
			print(line)

		# Extract Key
		result = re.search("desc\s*=\s*\"?([^\s\"{]+)\"?$", line)

		# Output
		if result:
			out.write(result.group(1) + '\n')

	text.close()


def main():

	# Parse Command Line Options
	parser = argparse.ArgumentParser()
	parser.add_argument('input'      , help = 'input folder')
	parser.add_argument('output'     , help = 'output file')
	parser.add_argument('--eu4'      , help = 'set for Europa Universalis IV', action = 'store_true')
	parser.add_argument('--ck2'      , help = 'set for Crusader Kings II'    , action = 'store_true')
	parser.add_argument('--hoi4'     , help = 'set for Hearts of Iron IV'    , action = 'store_true')
	parser.add_argument('--stellaris', help = 'set for Stellaris'            , action = 'store_true')
	parser.add_argument('--file'     , help = 'regard input as a file'       , action = 'store_true')
	parser.add_argument('--line'     , help = 'show processing lines'        , action = 'store_true')
	args = parser.parse_args()

	# Set Encording for Each Title
	if args.eu4:
		encord = 'ISO-8859-2'
	elif args.ck2:
		encord = 'utf_8'
	elif args.hoi4:
		encord = 'utf_8_sig'
	elif args.stellaris:
		encord = 'utf_8'

	# Analyze Target Files
	if (args.file):
		filepath = os.path.split(args.input)
		files = [filepath[1]]
		args.input = filepath[0]
	else:
		files = os.listdir(args.input)
	out = open(args.output, 'w', encoding = 'utf_8_sig')
	for file in files:
		print('Processing ' + file + '...')
		analyze(args.input, file, out, encord, args)
	out.close()


if __name__ == "__main__":
	# execute only if run as a script
	main()