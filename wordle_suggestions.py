import unittest

# regex para limpiar diccionario:
# ^[\wñáéíóúüÑÁÉÍÓÚÜ --,.']{6,}$\n
# ^[\wñáéíóúüÑÁÉÍÓÚÜ --,.']{0,4}$\n

def match_one_letter(position, letter, wordlist):
	suggestions = set()
	for w in wordlist:
		if w[position] == letter:
			suggestions.add(w)
	return suggestions

def match_letters(greenlist, wordlist):
	result = set(wordlist)
	for index, letter in greenlist:
		result = match_one_letter(index, letter, result)
	return result

def include_one_letter(position, letter, wordlist):
	suggestions = set()
	for w in wordlist:
		if letter in w and w[position] != letter:
			suggestions.add(w)
	return suggestions

def include_letters(yellowlist, wordlist):
	result = set(wordlist)
	for index, letter in yellowlist:
		result = include_one_letter(index, letter, result)
	return result

def exclude_one_letter(letter, wordlist):
	suggestions = set()
	for w in wordlist:
		if letter not in w:
			suggestions.add(w)
	return suggestions

def exclude_letters(greylist, wordlist):
	result = set(wordlist)
	for letter in greylist:
		result = exclude_one_letter(letter, result)
	return result

def all(colors, vocab):
	greylist = []
	yellowlist = []
	greenlist = []

	for i, color in enumerate(colors):
		if color[1] == 'G':
			greylist.append(color[0])
		elif color[1] == 'A':
			yellowlist.append((i, color[0]))
		else:
			greenlist.append((i, color[0]))

	vocab = exclude_letters(greylist, vocab)
	vocab = include_letters(yellowlist, vocab)
	vocab = match_letters(greenlist, vocab)
	return vocab

class TestWord(unittest.TestCase):
	def test_match_one_letter(self):
		vocab = {'oreas', 'oblea', 'libro', 'mural'}
		result = match_one_letter(0, 'o', vocab)
		self.assertSetEqual(result, {'oreas', 'oblea'})
	def test_match_letters(self):
		vocab = {'oreas', 'libro', 'mural', 'nivel', 'viral'}
		greenlist = [(3, 'a'), (4, 'l')]
		result = match_letters(greenlist, vocab)
		self.assertSetEqual(result, {'mural', 'viral'})
	def test_include_one_letter(self):
		vocab = {'oreas', 'libro', 'nuevo', 'nivel', 'viral'}
		result = include_one_letter(2, 'v', vocab)
		self.assertSetEqual(result, {'nuevo', 'viral'})
	def test_include_letters(self):
		vocab = {'valer', 'latón', 'vacío', 'mural', 'nivel', 'virar', 'libro'}
		yellowlist = [(3, 'a'), (4, 'l')]
		result = include_letters(yellowlist, vocab)
		self.assertSetEqual(result, {'valer', 'latón'})
	def test_exclude_one_letter(self):
		vocab = {'oreas', 'libro', 'nuevo', 'nivel', 'viral'}
		result = exclude_one_letter('o', vocab)
		self.assertSetEqual(result, {'nivel', 'viral'})
	def test_exclude_letters(self):
		vocab = {'valer', 'virar', 'libro', 'hurón', 'memez'}
		greylist = ['a', 'l']
		result = exclude_letters(greylist, vocab)
		self.assertSetEqual(result, {'memez', 'hurón'})
	def test_all(self):
		vocab = ['libro', 'rojas', 'olías', 'rosca', 'vejez', 'cubos']
		colors = [('o', 'A'), ('r', 'G'), ('e', 'G'), ('a', 'G'), ('s', 'V')]
		result = all(colors, vocab)
		self.assertSetEqual(result, {'cubos'})

result = [('o', 'A'), ('r', 'G'), ('e', 'G'), ('a', 'A'), ('s', 'A')]
with open('palabras_5.txt', 'r', encoding='UTF-8') as f:
	words = f.readlines()
	suggestions = all(result, words)
print(suggestions)

if __name__ == '__main__':
	unittest.main()