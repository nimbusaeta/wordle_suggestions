#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

# regex para limpiar diccionario:
# ^[\wñáéíóúüÑÁÉÍÓÚÜ --,.']{6,}$\n
# ^[\wñáéíóúüÑÁÉÍÓÚÜ --,.']{0,4}$\n
# ^.*[\.,/\-‒́' è].*$\n

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

def preguntar_idioma():
	idiomas_soportados = {"español": "es", "inglés": "en"}
	idioma = ""
	print("De momento este programa soporta los siguientes idiomas:")
	for idioma, código in idiomas_soportados.items():
		print(idioma, " (código: ", código, ")", sep="")
	print("¿En qué idioma estás jugando?")
	while idioma not in idiomas_soportados.values():
		idioma = input("Escribe el código correspondiente: ")
	return idioma

def preguntar():
	palabra = input("¿Qué palabra has puesto? ")
	colores = input("¿Qué secuencia de colores te ha salido? Escríbela así: GVAVG (G=gris, V=verde, A=amarillo) ")

	result = [(palabra[0], colores[0]),
			(palabra[1], colores[1]),
			(palabra[2], colores[2]),
			(palabra[3], colores[3]),
			(palabra[4], colores[4])]
	return result

def leer_vocab(idioma):
	archivo_idioma = 'en.txt'
	if idioma == 'es':
		archivo_idioma = 'es.txt'
	with open(archivo_idioma, 'r', encoding='UTF-8') as f:
		return f.readlines()

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

### PROGRAMA
suggestions = leer_vocab(preguntar_idioma())
suggestions = (s.lower() for s in suggestions)

continuar = True
while continuar:
	result = preguntar()
	suggestions = all(result, suggestions)
	print("Todas estas palabras cumplen los requisitos:")
	for suggestion in suggestions:
		print(suggestion.strip())

	if input("¿Continuar? Escribe 's' para seguir o cualquier otra cosa para salir: ") != "s":
		continuar = False



if __name__ == '__main__':
	unittest.main()