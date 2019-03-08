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

		# Skip Comment
		if (args.ck2 or args.hoi4 or args.stellaris):
			if re.match('^[\s]*#', line):
				continue

		# Extract Key
		if (args.eu4 or args.hoi4 or args.stellaris):
			result = re.search("^\s+([^\s:]+):", line)
		elif args.ck2:
			result = re.search("^([^;]+);", line)

		if result:
			key = result.group(1)
		else:
			key = None

		# Output
		if key:
			if not args.include:
				out.write(key + '\n')
			elif not key.find(args.include) == -1:
				out.write(key + '\n')

	text.close()


def main():

	# Parse Command Line Options
	parser = argparse.ArgumentParser()
	parser.add_argument('input'      , help = 'input folder')
	parser.add_argument('output'     , help = 'output file')
	parser.add_argument('--eu4'      , help = 'set for Europa Universalis IV'              , action = 'store_true')
	parser.add_argument('--ck2'      , help = 'set for Crusader Kings II'                  , action = 'store_true')
	parser.add_argument('--hoi4'     , help = 'set for Hearts of Iron IV'                  , action = 'store_true')
	parser.add_argument('--stellaris', help = 'set for Stellaris'                          , action = 'store_true')
	parser.add_argument('--include'  , help = 'extract keys include specified string'      , type = str)
	parser.add_argument('--append'   , help = 'append mode (not overwrite)'                , action = 'store_true')
	parser.add_argument('--file'     , help = 'regard input as a file'                     , action = 'store_true')
	parser.add_argument('--line'     , help = 'show processing lines'                      , action = 'store_true')
	args = parser.parse_args()

	# Set Encording for Each Title
	if args.eu4:
		encord = 'utf_8_sig'
	elif args.ck2:
		encord = 'ISO-8859-1'
	elif args.hoi4:
		encord = 'utf_8_sig'
	elif args.stellaris:
		encord = 'utf_8_sig'

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
		analyze(folder, file, out, encord, args)
	out.close()


if __name__ == "__main__":
	# execute only if run as a script
	main()
