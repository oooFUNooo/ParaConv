import os
import sys
import csv
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *


def convertVerbForm(dic, word, form):

	return dic.get(word + ':' + form)


def analyze(path, file, out, log, dic):

	# Prepare to Analyze
	char_filters = [RegexReplaceCharFilter('\[.*\]', ''),
					RegexReplaceCharFilter('§.', ''),
					]

	tokenizer = Tokenizer()

	analyzer = Analyzer(char_filters, tokenizer)

	text = open(path + '/' + file, 'r', encoding = 'UTF-8')

	# Analyze
	for line in text:

		# For Logging
		logflag = False
		srcline = line

		# Remove Line Feed
		line = line.rstrip('\n')

		# Skip Header
		if (line == 'l_english:'):
			out.write(line + '\n')
			continue

		# Split into Sentences
		maintext = line.split('"')[1].split('"')[0]
		sentences = maintext.split('。')

		# Break into Tokens
		for sentence in sentences:
			tokens = analyzer.analyze(sentence)

			# Initialize
			preword    = ''
			prepreword = ''
			preform    = ''
			prepreform = ''
			prepart    = ['','','','','','','','','']
			preprepart = ['','','','','','','','','']

			# Apply Rules
			for token in tokens:

				word = token.surface
				form = token.infl_form
				part = token.part_of_speech.split(',')[0]
				convsrc = ''
				convdst = ''

				print(word, form, part)

				# Rule 1
				if (part == '動詞' and form == '基本形'):
					convsrc = word
					convdst = dic.get(word + ':' + '連用形') + 'ます'

				# Replace words
				if not convsrc == '':
					logflag = True
					line = line.replace(convsrc, convdst, 1)

				# Shift Parameters
				prepreword = preword
				prepreform = preform
				preprepart = prepart
				preword    = word
				preform    = form
				prepart    = part

		# Output
		out.write(line + '\n')

		# Logging
		if logflag:
			log.write('- ' + srcline)
			log.write('+ ' + line + '\n')

	text.close()


def main():

	# Process Command Line Options
	target = sys.argv[1] # Target Folder
	output = sys.argv[2] # Output Folder
	result = sys.argv[3] # Result Folder

	# Create Verb Dictionary
	verbdic = {}
	dic = open('Verb.csv', 'r', encoding = 'EUC-JP')
	dataReader = csv.reader(dic)
	for row in dataReader:
		verbdic[row[10] + ':' + row[9]] = row[0]
	dic.close()

	# Create Folders
	if not os.path.isdir(output):
		os.mkdir(output)
	if not os.path.isdir(result):
		os.mkdir(result)

	# Analyze Target Files
	files = os.listdir(target)
	for file in files:
		out = open(output + '/' + file, 'w', encoding = 'UTF-8')
		log = open(result + '/' + file, 'w', encoding = 'UTF-8')
		analyze(target, file, out, log, verbdic)
		out.close()
		log.close()


if __name__ == "__main__":
	# execute only if run as a script
	main()
