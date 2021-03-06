import os
import re
import time
import requests
import argparse
import urllib.parse


transdic = {}
includekeylist = []
excludekeylist = []

headers = {
	'Connection': 'keep-alive',
}


def createTranslatedDictionary(file, args):

	for line in file:

		# Skip Comment
		if (args.ck2 or args.hoi4 or args.stellaris):
			if re.match(r'^[\s]*#', line):
				continue

		# Skip No Main Text
		if (args.eu4 or args.hoi4 or args.stellaris):
			if line.find('"') == -1:
				continue
		elif args.ck2:
			if line.find(';') == -1:
				continue

		# Check Key
		if (args.eu4 or args.hoi4 or args.stellaris):
			key = re.search(r"^\s*([^\s:]+):", line).group(1)
		elif args.ck2:
			key = re.search(r"^([^;]+);", line).group(1)

		# Extract Main Text
		if (args.eu4 or args.hoi4 or args.stellaris):
			maintext = line.split('"')[1].split('"')[0]
		elif args.ck2:
			maintext = line.split(';')[1].split(';')[0]

		transdic[key] = maintext


def translate(path, file, out, encode, args):

	outputflag = False
	text = open(path + '/' + file, 'r', encoding = encode)

	# Translate
	for line in text:

		# Remove Line Feed
		line = line.rstrip('\n')

		# Skip Comment
		if (args.ck2 or args.hoi4 or args.stellaris):
			if re.match(r'^[\s]*#', line):
				out.write(line + '\n')
				continue

		# Skip No Main Text 1
		if (args.eu4 or args.hoi4 or args.stellaris):
			if line.find('"') == -1:
				out.write(line + '\n')
				continue
			else:
				maintext = line.split('"')[1].split('"')[0]
		elif args.ck2:
			if line.find(';') == -1:
				out.write(line + '\n')
				continue
			else:
				maintext = line.split(';')[1].split(';')[0]

		# Check Key
		if (args.eu4 or args.hoi4 or args.stellaris):
			key = re.search(r"^\s*([^\s:]+):", line).group(1)
		elif args.ck2:
			key = re.search(r"^([^;]+);", line).group(1)

		# Skip No Main Text 2
		if re.match(r'^\s*$', maintext):
			if not args.difference:
				out.write(line + '\n')
				outputflag = True
			continue

		# Skip Not Specified Keys 1
		if args.key:
			if not key in includekeylist:
				if (args.translated and transdic.get(key) and not transdic.get(key) == maintext):
					line = line.replace(maintext, transdic.get(key))
				if not args.difference:
					out.write(line + '\n')
					outputflag = True
				continue

		# Skip Not Specified Keys 2
		if args.keyexclude:
			if key in excludekeylist:
				if (args.translated and transdic.get(key) and not transdic.get(key) == maintext):
					line = line.replace(maintext, transdic.get(key))
				if not args.difference:
					out.write(line + '\n')
					outputflag = True
				continue

		# Skip Translated Keys
		if args.translated:
			if transdic.get(key) and not transdic.get(key) == maintext:
				line = line.replace(maintext, transdic.get(key))
				if not args.difference:
					out.write(line + '\n')
					outputflag = True
				continue

		# For Debug Purpose
		if args.line:
			print(line)

		# Escape Special Texts
		srctext = maintext
		escapedic = {}
		counter = 0;

		while True:

			escapestring = 'ESC' + format(counter, '04d')

			if re.search('\\\\n', maintext):
				src = '\\n'

			elif re.search('¤', maintext):
				src = '¤'

			elif re.search('§.', maintext):
				src = re.search('§.', maintext).group()

			elif re.search(r'£[^\s]+\s', maintext):
				src = re.search(r'£[^\s]+\s', maintext).group()

			elif re.search(r'@\$[^\$]+\$', maintext):
				src = re.search(r'@\$[^\$]+\$', maintext).group()

			elif re.search(r'\$[^\$]+\$', maintext):
				src = re.search(r'\$[^\$]+\$', maintext).group()

			elif re.search(r'\[[^\]]+\]', maintext):
				src = re.search(r'\[[^\]]+\]', maintext).group()

			else:
				break

			maintext = maintext.replace(src, ' ' + escapestring + ' ', 1)
			escapedic[escapestring] = src
			counter = counter + 1

		# Call Translator
		response = requests.get(args.url + urllib.parse.quote(maintext) + urllib.parse.unquote(args.urloption), headers = headers)
		if not response:
			continue
		transtext = response.text

		# Unescape Special Texts
		for escapestring in escapedic:

			src = escapedic.get(escapestring)

			if re.search(r'£[^\s]+\s', src):
				src = re.sub(r'(£[^\s]+)\s', r'\1£', src)

			transtext = transtext.replace( escapestring, src )

		# Post Processing
		transtext = transtext.replace(' ', '')

		if args.mark:
			transtext = '（自動翻訳）' + transtext

		# Output
		line = line.replace(srctext, transtext)
		out.write(line + '\n')
		outputflag = True

		# Wait
		time.sleep(0.1)

	text.close()

	return outputflag


def main():

	# Parse Command Line Options
	parser = argparse.ArgumentParser()
	parser.add_argument('input'       , help = 'input folder')
	parser.add_argument('output'      , help = 'output folder')
	parser.add_argument('--eu4'       , help = 'set for Europa Universalis IV'              , action = 'store_true')
	parser.add_argument('--ck2'       , help = 'set for Crusader Kings II'                  , action = 'store_true')
	parser.add_argument('--hoi4'      , help = 'set for Hearts of Iron IV'                  , action = 'store_true')
	parser.add_argument('--stellaris' , help = 'set for Stellaris'                          , action = 'store_true')
	parser.add_argument('--url'       , help = 'specify translator\'s URL (before text)'    , type = str)
	parser.add_argument('--urloption' , help = 'specify translator\'s options (after text)' , type = str)
	parser.add_argument('--translated', help = 'specify translated text folder'             , type = str)
	parser.add_argument('--key'       , help = 'supply a key file for include'              , type = str)
	parser.add_argument('--keyinclude', help = 'supply a key file for include (same as key)', type = str)
	parser.add_argument('--keyexclude', help = 'supply a key file for exclude'              , type = str)
	parser.add_argument('--difference', help = 'output differences only'                    , action = 'store_true')
	parser.add_argument('--file'      , help = 'regard input as a file'                     , action = 'store_true')
	parser.add_argument('--mark'      , help = 'mark as translated'                         , action = 'store_true')
	parser.add_argument('--line'      , help = 'show processing lines'                      , action = 'store_true')
	args = parser.parse_args()

	# Set Encoding for Each Title
	if args.eu4:
		encode = 'utf_8_sig'
	elif args.ck2:
		encode = 'ISO-8859-1'
	elif args.hoi4:
		encode = 'utf_8_sig'
	elif args.stellaris:
		encode = 'utf_8_sig'

	# Create Translated Keys Dictionary
	if args.translated:
		found = []
		for root, dirs, files in os.walk(args.translated):
			for filename in files:
				found.append(os.path.join(root, filename))
		for path in found:
			f = open(path, 'r', encoding = encode)
			createTranslatedDictionary(f, args)
			f.close()

	# Create Include Key List
	if args.keyinclude:
		args.key = args.keyinclude

	if args.key:
		keys = open(args.key, 'r', encoding = 'utf_8_sig')
		for key in keys:
			key = key.rstrip('\n')
			includekeylist.append(key)
		keys.close()

	# Create Exclude Key List
	if args.keyexclude:
		keys = open(args.keyexclude, 'r', encoding = 'utf_8_sig')
		for key in keys:
			key = key.rstrip('\n')
			excludekeylist.append(key)
		keys.close()

	# Create Folders
	if not os.path.isdir(args.output):
		os.mkdir(args.output)

	# Translate Target Files
	if (args.file):
		found = [args.input]
	else:
		found = []
		for root, dirs, files in os.walk(args.input):
			for filename in files:
				found.append(os.path.join(root, filename))
	for path in found:
		file   = os.path.basename(path)
		folder = os.path.dirname (path)
		print('Processing ' + file + '...')
		outfilename = args.output + '/' + file
		out = open(outfilename, 'w', encoding = encode)
		outputflag = translate(folder, file, out, encode, args)
		out.close()
		if not outputflag:
			os.remove(outfilename)


if __name__ == "__main__":
	# execute only if run as a script
	main()
