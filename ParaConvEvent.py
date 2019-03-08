import os
import re
import argparse


def analyze(path, file, out, encode, args):

	text = open(path + '/' + file, 'r', encoding = encode)

	# Analyze
	for line in text:

		# Remove Line Feed
		line = line.rstrip('\n')

		# For Debug Purpose
		if args.line:
			print(line)

		# Extract Key
		result = re.search(r"desc\s*=\s*\"?([^\s\"{]+)\"?$", line)

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
	parser.add_argument('--append'   , help = 'append mode (not overwrite)'  , action = 'store_true')
	parser.add_argument('--file'     , help = 'regard input as a file'       , action = 'store_true')
	parser.add_argument('--line'     , help = 'show processing lines'        , action = 'store_true')
	args = parser.parse_args()

	# Set encoding for Each Title
	if args.eu4:
		encode = 'ISO-8859-2'
	elif args.ck2:
		encode = 'utf_8'
	elif args.hoi4:
		encode = 'utf_8_sig'
	elif args.stellaris:
		encode = 'utf_8'

	# Analyze Target Files
	if (args.file):
		found = [args.input]
	else:
		found = []
		for root, dirs, files in os.walk(args.input):
			for filename in files:
				found.append(os.path.join(root, filename))
	if (args.append):
		out = open(args.output, 'a', encoding = 'utf_8_sig')
	else:
		out = open(args.output, 'w', encoding = 'utf_8_sig')
	for path in found:
		file   = os.path.basename(path)
		folder = os.path.dirname (path)
		print('Processing ' + file + '...')
		analyze(folder, file, out, encode, args)
	out.close()


if __name__ == "__main__":
	# execute only if run as a script
	main()
