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
			word       = ''
			preword    = ''
			prepreword = ''
			base       = ''
			prebase    = ''
			preprebase = ''
			form       = ''
			preform    = ''
			prepreform = ''
			part       = ['','','','','','','','','']
			prepart    = ['','','','','','','','','']
			preprepart = ['','','','','','','','','']
			convsrc    = ''
			convdst    = ''

			# Apply Rules
			for token in tokens:

				# Shift Parameters
				prepreword = preword
				preprebase = prebase
				prepreform = preform
				preprepart = prepart
				preword    = word
				prebase    = base
				preform    = form
				prepart    = part

				# Get Parameters
				word = token.surface
				base = token.base_form
				form = token.infl_form
				part = token.part_of_speech.split(',')[0]

				# Rule 12
				if ((base == 'だ' or base == 'だが') and part == '接続詞'):
					convsrc = word
					convdst = 'ですが'

				# Replace words
				if not convsrc == '':
					logflag = True
					line = line.replace(convsrc, convdst, 1)
					convsrc == ''

			else:

				# Rule 1
				if (part == '動詞' and form == '基本形'):
					convsrc = word
					convdst = dic.get(base + ':' + '連用形') + 'ます'

				# Rule 2
				elif (prepart == '動詞' and (preform == '連用形' or preform == '連用タ接続') and base == 'た' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = dic.get(prebase + ':' + '連用形') + 'ました'

				# Rule 3
				elif (prepart == '動詞' and preform == '未然形' and base == 'ない' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = dic.get(prebase + ':' + '未然形') + 'ません'

				# Rule 4
				elif (preprepart == '動詞' and prepreform == '未然形' and prebase == 'ない' and prepart == '助動詞' and preform == '連用タ接続' and base == 'た' and part == '助動詞' and form == '基本形'):
					convsrc = prepreword + preword + word
					convdst = dic.get(preprebase + ':' + '未然形') + 'ませんでした'

				# Rule 5
				elif (base == 'だ' and part == '助動詞' and form == '基本形'):
					convsrc = word
					convdst = 'です'

				# Rule 6
				elif (prebase == 'だ' and prepart == '助動詞' and preform == '連用タ接続' and base == 'た' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = 'でした'

				# Rule 7
				elif (base == 'ない' and part == '助動詞' and form == '基本形'):
					convsrc = word
					convdst = 'ありません'

				# Rule 8
				elif (prebase == 'だ' and prepart == '助動詞' and preform == '連用形' and base == 'ある' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = 'です'

				# Rule 9
				elif (preprebase == 'だ' and preprepart == '助動詞' and prepreform == '連用形' and prebase == 'ある' and prepart == '助動詞' and preform == '連用タ接続' and base == 'た' and part == '助動詞' and form == '基本形'):
					convsrc = prepreword + preword + word
					convdst = 'でした'

				# Rule 10
				elif (preprebase == 'だ' and preprepart == '助動詞' and prepreform == '連用形' and prebase == 'ある' and prepart == '助動詞' and preform == '未然ウ接続' and base == 'う' and part == '助動詞' and form == '基本形'):
					convsrc = prepreword + preword + word
					convdst = 'でしょう'

				# Rule 11
				elif (prebase == 'だ' and prepart == '助動詞' and preform == '未然形' and base == 'う' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = 'でしょう'

				# Rule 13
				elif (base == 'ない' and part == '形容詞' and form == '基本形'):
					convsrc = word
					convdst = 'ありません'

				# Rule 14
				elif (prebase == 'ない' and prepart == '形容詞' and preform == '連用タ接続' and base == 'た' and part == '助動詞' and form == '基本形'):
					convsrc = preword + word
					convdst = 'ありませんでした'

				# Replace words
				if not convsrc == '':
					logflag = True
					line = line.replace(convsrc, convdst, 1)

		# Output
		out.write(line + '\n')

		# Logging
		if logflag:
			log.write('- ' + srcline)
			log.write('+ ' + line + '\n\n')

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
