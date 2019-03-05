import os
import re
import csv
import random
import argparse
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *


verbdic = {}
keylist = []
we_exceptions = {'だけ'}
mashita_exceptions = ['する', 'せる', 'いる', 'くる']


def convertVerbForm(word, form):

	ret = verbdic.get(word + ':' + form)
	if (ret == None and form == '連用タ接続'):
		form = '連用形'
		ret = verbdic.get(word + ':' + '連用形')
	if (ret == None and form == '連用形'):
		form = '未然形'
		ret = verbdic.get(word + ':' + '未然形')
	return ret


def applyJoutaiToKeitaiRule(line, analyzer, args):

	# Split into Sentences
	if (args.eu4 or args.hoi4 or args.stellaris):
		maintext = line.split('"')[1].split('"')[0]
	elif (args.ck2):
		maintext = line.split(';')[1].split(';')[0]

	sentences = re.split('[。？！…]', maintext)

	# Break into Tokens
	for sentence in sentences:
		tokens = analyzer.analyze(sentence)
		srcsentence = sentence

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

			# For Debug Purpose
			if args.token:
				print(word, base, part, form)

			# Rule 12
			if ((prebase == 'だ' or prebase == 'だが') and prepart == '接続詞'):
				convsrc = preword + word
				convdst = 'ですが' + word

			# Replace Words
			if not convsrc == '':
				sentence = sentence.replace(convsrc, convdst, 1)
				convsrc = ''

		else:

			# Rule 1
			if (part == '動詞' and form == '基本形'):
				convsrc = word
				convdst = convertVerbForm(base, '連用形') + 'ます'

			# Rule 2
			elif (prepart == '動詞' and (preform == '連用形' or preform == '連用タ接続') and base == 'た' and part == '助動詞' and form == '基本形'):
				convsrc = preword + word
				convdst = convertVerbForm(prebase, '連用形') + 'ました'

			# Rule 3
			elif (prepart == '動詞' and preform == '未然形' and base == 'ない' and part == '助動詞' and form == '基本形'):
				convsrc = preword + word
				convdst = convertVerbForm(prebase, '連用形') + 'ません'

			# Rule 4
			elif (preprepart == '動詞' and prepreform == '未然形' and prebase == 'ない' and prepart == '助動詞' and preform == '連用タ接続' and base == 'た' and part == '助動詞' and form == '基本形'):
				convsrc = prepreword + preword + word
				convdst = convertVerbForm(preprebase, '連用形') + 'ませんでした'

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

			# Replace Words Backward
			if not convsrc == '':
				sentence = sentence[::-1]
				convsrc  = convsrc[::-1]
				convdst  = convdst[::-1]
				sentence = sentence.replace(convsrc, convdst, 1)
				sentence = sentence[::-1]
				line = line.replace(srcsentence, sentence, 1)

	return line


def applyKeitaiToJoutaiRule(line, analyzer, args):

	# Split into Sentences
	if (args.eu4 or args.hoi4 or args.stellaris):
		maintext = line.split('"')[1].split('"')[0]
	elif args.ck2:
		maintext = line.split(';')[1].split(';')[0]

	sentences = re.split('[。？！…]', maintext)
	srcline = line

	# Break into Tokens
	for sentence in sentences:
		tokens = analyzer.analyze(sentence)
		srcsentence = sentence

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

			# For Debug Purpose
			if args.token:
				print(token.surface, token.base_form, token.part_of_speech.split(',')[0], token.infl_form)

			# Join Tokens
			if (part == '助動詞' and token.part_of_speech.split(',')[0] == '助動詞'):
				word = word + token.surface

			else:

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

			# Rule 7/13
			if (preprebase == 'ある' and (preprepart == '動詞' or preprepart == '形容詞') and prepreform == '連用形' and preword == 'ません' and prepart == '助動詞' and part != '助動詞'):
				convsrc = prepreword + preword + word
				convdst = 'ない' + word

			# Rule 14
			elif (prebase == 'ある' and (prepart == '動詞' or prepart == '形容詞') and preform == '連用形' and word == 'ませんでした' and part == '助動詞'):
				convsrc = preword + word
				convdst = 'なかった'

			# Rule 3
			elif (preprepart == '動詞' and prepreform == '連用形' and 'ません' in preword and prepart == '助動詞' and part != '助動詞'):
				convsrc = prepreword + preword.replace('ません', '') + 'ません' + word
				convdst = convertVerbForm(preprebase, '未然形') + preword.replace('ません', '') + 'ない' + word

			# Rule 4
			elif (prepart == '動詞' and preform == '連用形' and 'ませんでした' in word and part == '助動詞'):
				convsrc = preword + word.replace('ませんでした', '') + 'ませんでした'
				convdst = convertVerbForm(prebase, '未然形') + word.replace('ませんでした', '') + 'なかった'

			# Rule 1
			elif (prepart == '動詞' and preform == '連用形' and word == 'ます' and part == '助動詞'):
				convsrc = preword + word
				convdst = convertVerbForm(prebase, '基本形')

			# Rule 2
			elif (prepart == '動詞' and preform == '連用形' and word == 'ました' and part == '助動詞'):
				convsrc = preword + word
				if prebase in mashita_exceptions:
					verb = convertVerbForm(prebase, '連用形')
				else:
					verb = convertVerbForm(prebase, '連用タ接続')
				if verb[-1:] == 'ん':
					tada = 'だ'
				else:
					tada = 'た'
				convdst = verb + tada

			# Rule 12
			elif (prebase == 'ですが' and prepart == '接続詞'):
				convsrc = preword + word
				convdst = 'だが' + word

			# Replace Words
			if not convsrc == '':
				sentence = sentence.replace(convsrc, convdst, 1)
				convsrc = ''

		else:

			# Check the end of a sentence to force 'dearu'
			if (args.dearu):
				pos = srcline.find(sentence)
				if (pos + len(sentence) < len(srcline) and (srcline[pos + len(sentence)] == '！' or srcline[pos + len(sentence)] == '…')):
					dearuflag = False
				else:
					dearuflag = True

			# Rule 7/13
			if (prebase == 'ある' and (prepart == '動詞' or prepart == '形容詞') and preform == '連用形' and word == 'ません' and part == '助動詞'):
				convsrc = preword + word
				convdst = 'ない'

			# Rule 3
			elif (prepart == '動詞' and preform == '連用形' and 'ません' in word and part == '助動詞'):
				convsrc = preword + word.replace('ません', '') + 'ません'
				convdst = convertVerbForm(prebase, '未然形') + word.replace('ません', '') + 'ない'

			# Rule 5/8 Another Version
			elif (prepart == '形容詞' and preform == '基本形' and 'です' in word and part == '助動詞'):
				convsrc = preword + word
				convdst = preword

			# Rule 5/8
			elif ('です' in word and part == '助動詞'):
				convsrc = 'です'
				if args.da:
					convdst = 'だ'
				elif args.dearu:
					convdst = 'である'
				else:
					convdst = random.choice(['だ', 'である'])

			# Rule 6/9
			elif ('でした' in word and part == '助動詞'):
				convsrc = 'でした'
				if args.da:
					convdst = 'だった'
				elif args.dearu:
					convdst = 'であった'
				else:
					convdst = random.choice(['だった', 'であった'])

			# Rule 10/11
			elif ('でしょう' in word and part == '助動詞'):
				convsrc = 'でしょう'
				if args.da:
					convdst = 'だろう'
				elif args.dearu:
					convdst = 'であろう'
				else:
					convdst = random.choice(['だろう', 'であろう'])

			# Rule 5/8 Forced
			elif (args.da and word[-3:] == 'である' and part == '助動詞'):
				convsrc = word
				convdst = word[:-3] + 'だ'
			elif (args.dearu and word[-1:] == 'だ' and part == '助動詞' and dearuflag):
				convsrc = word
				convdst = word[:-1] + 'である'

			# Rule 6/9 Forced
			elif (args.da and word[-4:] == 'であった' and part == '助動詞'):
				convsrc = word
				convdst = word[:-4] + 'だった'
			elif (args.dearu and word[-3:] == 'だった' and part == '助動詞'):
				convsrc = word
				convdst = word[:-3] + 'であった'

			# Rule 10/11 Forced
			elif (args.da and word[-4:] == 'であろう' and part == '助動詞'):
				convsrc = word
				convdst = word[:-4] + 'だろう'
			elif (args.dearu and word[-3:] == 'だろう' and part == '助動詞'):
				convsrc = word
				convdst = word[:-3] + 'であろう'

			# Replace Words
			if not convsrc == '':
				sentence = sentence[::-1]
				convsrc  = convsrc[::-1]
				convdst  = convdst[::-1]
				sentence = sentence.replace(convsrc, convdst, 1)
				sentence = sentence[::-1]

			line = line.replace(srcsentence, sentence, 1)

	return line


def applyNoPronounRule(line, analyzer, args):

	# Split into Sentences
	if (args.eu4 or args.hoi4 or args.stellaris):
		maintext = line.split('"')[1].split('"')[0]
	elif args.ck2:
		maintext = line.split(';')[1].split(';')[0]

	sentences = re.split('[。？！…]', maintext)

	# Break into Tokens
	for sentence in sentences:
		tokens = analyzer.analyze(sentence)
		srcsentence = sentence

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

			# For Debug Purpose
			if args.token:
				print(word, base, part, form)

			# Rule A-1
			if (preword == '我々' and part == '助詞' and (not base in we_exceptions)):
				convsrc = preword + word
				convdst = ''

			# Rule A-2
			if (prepreword == '私' and (preword == 'たち' or preword == '達') and part == '助詞' and (not base in we_exceptions)):
				convsrc = prepreword + preword + word
				convdst = ''

			# Rule B-1
			if (preword == '彼ら' and (word == 'が' or word == 'は')):
				convsrc = preword + word
				convdst = ''

			# Rule B-2
			if (preword == '彼ら' and word == 'の'):
				convsrc = preword + word
				convdst = 'その'

			# Rule B-3
			if (preword == '彼ら' and word == '自身'):
				convsrc = preword + word
				convdst = '自分自身'

			# Replace Words
			if not convsrc == '':

				# Check the next letter is comma or not
				p = sentence.find(convsrc)
				if (p + len(convsrc) < len(sentence) and (sentence[p + len(convsrc)] == '、')):
					convsrc = convsrc + '、'
				
				sentence = sentence.replace(convsrc, convdst, 1)
				convsrc = ''

		line = line.replace(srcsentence, sentence, 1)

	# Rule B-1 Another Version
	line = re.sub("\[[^\[\]]+\.GetSheHe[^\]]*\][がは]、?", '', line)

	# Rule B-2 Another Version
	line = re.sub("\[[^\[\]]+\.GetHerHis[^\]]*\]の、?", 'その', line)

	# Rule B-3 Another Version
	line = re.sub("\[[^\[\]]+\.GetHerselfHimself[^\]]*\]、?", '自分自身', line)

	return line


def applyExceptionRule(line, key, args):

	# Exceptions for Europa Universalis IV
	if args.eu4:

		if key == 'consort_events.3.d':
			line = line.replace('（および[Root.Monarch.GetHerHis]の）', '')

	return line


def analyze(path, file, out, log, args):

	outputflag = False

	# Prepare to Analyze
	char_filters = [RegexReplaceCharFilter('\[[^\[\]]+\]', ''),
					RegexReplaceCharFilter('§.', ''),
					]

	tokenizer = Tokenizer()

	analyzer = Analyzer(char_filters, tokenizer)

	text = open(path + '/' + file, 'r', encoding = 'utf_8_sig')

	# Analyze
	for line in text:

		# Remove Line Feed
		line = line.rstrip('\n')
		linesrc = line

		# Skip No Main Text
		if (args.eu4 or args.hoi4 or args.stellaris):
			if line.find('"') == -1:
				out.write(line + '\n')
				continue
		elif args.ck2:
			if line[0] == '#':
				out.write(line + '\n')
				continue

		# Check Key
		if (args.eu4 or args.hoi4 or args.stellaris):
			key = re.search("^\s*([^\s:]+):", line).group(1)
		elif args.ck2:
			key = re.search("^([^;]+);", line).group(1)

		if args.key:
			if not key in keylist:
				if not args.difference:
					outputflag = True
					out.write(line + '\n')
				continue

		# For Debug Purpose
		if args.line:
			print(line)

		# Apply Rules
		if not args.noexception:
			line = applyExceptionRule(line, key, args)
		if args.keitai:
			line = applyJoutaiToKeitaiRule(line, analyzer, args)
		if args.joutai:
			line = applyKeitaiToJoutaiRule(line, analyzer, args)
		if args.nopronoun:
			line = applyNoPronounRule(line, analyzer, args)

		# Logging
		if not line == linesrc:
			log.write('- ' + linesrc + '\n')
			log.write('+ ' + line    + '\n\n')

		# Output
		if (not args.difference or not line == linesrc):
			outputflag = True
			if (not args.original or line == linesrc):
				if (not args.mark or line == linesrc):
					out.write(line + '\n')
				else:
					if (args.eu4 or args.hoi4 or args.stellaris):
						maintext = line.split('"')[1].split('"')[0]
						line = re.sub("\"[^\"]+\"", '\"' + maintext + '\\\\n\\\\n\* ' + key + '\"', line, 1)
					elif args.ck2:
						maintext = line.split(';')[1].split(';')[0]
						line = re.sub("^([^;]*);[^;]+;", linesrc.split(';')[0] + ';' + maintext + '\\\\n\\\\n\* ' + key + ';', line, 1)
					out.write(line + '\n')
			else:
				if (args.eu4 or args.hoi4 or args.stellaris):
					maintext    = line   .split('"')[1].split('"')[0]
					maintextsrc = linesrc.split('"')[1].split('"')[0]
				elif args.ck2:
					maintext    = line   .split(';')[1].split(';')[0]
					maintextsrc = linesrc.split(';')[1].split(';')[0]
				maintext    = maintext   .replace('\\n', '\\\\n')
				maintextsrc = maintextsrc.replace('\\n', '\\\\n')
				if (args.eu4 or args.hoi4 or args.stellaris):
					line = re.sub("\"[^\"]+\"", "\"" + maintext + '\\\\n\\\\n＜原文＞\\\\n' + maintextsrc + '\"', line, 1)
				elif args.ck2:
					line = re.sub("^([^;]*);[^;]+;", linesrc.split(';')[0] + ";" + maintext + '\\\\n\\\\n＜原文＞\\\\n' + maintextsrc + ';', line, 1)
				out.write(line + '\n')

	text.close()

	return outputflag


def main():

	# Parse Command Line Options
	parser = argparse.ArgumentParser()
	parser.add_argument('input'        , help = 'input folder')
	parser.add_argument('output'       , help = 'output folder')
	parser.add_argument('log'          , help = 'log folder')
	parser.add_argument('--eu4'        , help = 'for Europa Universalis IV'       , action = 'store_true')
	parser.add_argument('--ck2'        , help = 'for Crusader Kings II'           , action = 'store_true')
	parser.add_argument('--hoi4'       , help = 'for Hearts of Iron IV'           , action = 'store_true')
	parser.add_argument('--stellaris'  , help = 'for Stellaris'                   , action = 'store_true')
	parser.add_argument('--keitai'     , help = 'convert into keitai (desu, masu)', action = 'store_true')
	parser.add_argument('--joutai'     , help = 'convert into joutai (da, dearu)' , action = 'store_true')
	parser.add_argument('--da'         , help = 'convert into joutai (da only)'   , action = 'store_true')
	parser.add_argument('--dearu'      , help = 'convert into joutai (dearu only)', action = 'store_true')
	parser.add_argument('--nopronoun'  , help = 'omit useless pronouns'           , action = 'store_true')
	parser.add_argument('--difference' , help = 'output differences only'         , action = 'store_true')
	parser.add_argument('--original'   , help = 'output with original texts'      , action = 'store_true')
	parser.add_argument('--mark'       , help = 'mark as converted'               , action = 'store_true')
	parser.add_argument('--key'        , help = 'supply a key file'               , type = str)
	parser.add_argument('--file'       , help = 'regard input as a file'          , action = 'store_true')
	parser.add_argument('--line'       , help = 'show processing lines'           , action = 'store_true')
	parser.add_argument('--token'      , help = 'show processing tokens'          , action = 'store_true')
	parser.add_argument('--noexception', help = 'accept no exceptions'            , action = 'store_true')

	args = parser.parse_args()
	if (args.da or args.dearu):
		args.joutai = True

	# Create Key List
	if args.key:
		keys = open(args.key, 'r', encoding = 'utf_8_sig')
		for key in keys:
			key = key.rstrip('\n')
			keylist.append(key)
		keys.close()

	# Create Verb Dictionary
	print('Creating dictionary...')
	dic = open('Verb.csv', 'r', encoding = 'EUC-JP')
	dataReader = csv.reader(dic)
	for row in dataReader:
		verbdic[row[10] + ':' + row[9]] = row[0]
	dic.close()

	# Create Folders
	if not os.path.isdir(args.output):
		os.mkdir(args.output)
	if not os.path.isdir(args.log):
		os.mkdir(args.log)

	# Analyze Target Files
	if (args.file):
		filepath = os.path.split(args.input)
		files = [filepath[1]]
		args.input = filepath[0]
	else:
		files = os.listdir(args.input)
	for file in files:
		print('Processing ' + file + '...')
		outfilename = args.output + '/' + file
		logfilename = args.log    + '/' + file + '.diff'
		out = open(outfilename, 'w', encoding = 'utf_8_sig')
		log = open(logfilename, 'w', encoding = 'utf_8_sig')
		outputflag = analyze(args.input, file, out, log, args)
		out.close()
		log.close()
		if not outputflag:
			os.remove(outfilename)
		if os.path.getsize(logfilename) == 0:
			os.remove(logfilename)


if __name__ == "__main__":
	# execute only if run as a script
	main()
