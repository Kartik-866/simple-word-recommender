from os import listdir
from getch import getch
import sys



PATH = 'NLPBooks/'
stopwords = '.,-_&?><~!@#$%^&*():\';1234567890'

dictionary = {}
for file in listdir(path=PATH):
	with open(PATH + file) as fr:
		sentences = fr.read()
		for char in stopwords:
			sentences = sentences.replace(char, '')
		sentences = sentences.split()

		for word in sentences:
			dictionary[word] = (dictionary[word] + 1) if word in dictionary else 1


print('Enter some text: ', end='')
sys.stdout.flush()

word = ''
sentence = ['']
sub_dict = dictionary.copy()
suggestions = []
count = 0

while True:
	letter = getch()

	print('\b' * count, end='')
	print(' ' * count, end='')
	print('\b' * count, end='')

	if letter == ' ':
		sub_dict = dictionary.copy()
		print('\033[1m' + ' '.join(sentence), end=' ')
		sentence.append('')
		word = ''
		sys.stdout.flush()
		count += 1
		continue
	elif letter == '\t':
		sub_dict = dictionary.copy()
		word = suggestions[0][1]
		sentence[-1] = word
		print('\033[1m' + ' '.join(sentence), end=' ')
		sys.stdout.flush()
		sentence.append('')
		word = ''
		count += 1
		continue
	elif letter == '\n':
		print()
		print(' '.join(sentence))
		break
	elif ord(letter) == 127:
		sys.stdout.flush()
		word = word[:-1]
		sentence[-1] = word
		sub_dict = dictionary.copy()
	else:
		word += letter
		sentence[-1] = word

	suggestions.clear()
	for key in sub_dict:
		if key.startswith(word):
			suggestions.append((sub_dict[key], key))
	suggestions.sort(reverse=True)

	sub_dict.clear()
	for sug in suggestions:
		sub_dict[sug[1]] = sug[0]

	print('\033[1m' + ' '.join(sentence) + '\033[0m', end='')
	print(suggestions[0][1][len(word):], end='')
	sys.stdout.flush()
	count = len(' '.join(sentence) + suggestions[0][1][len(word):])
