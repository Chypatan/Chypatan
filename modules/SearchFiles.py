import os

class SearchFiles:
	def __init__(self, path='./.'):
		self.path = path
		
	def search(self, extension, word=''):
		number = 1
		a = []
		for root, dirs, files in os.walk(self.path):
			for i in files:
				if i.endswith(extension):
					#i=i.lower()
					if i.find(word) != -1:
						a.append(i)
						number += 1
		return a

if __name__ == '__main__':
	a = SearchFiles('/storage/emulated/0').search(str(input('Расширение файла - ')), str(input('Ключевое слово или часть слова (маленькими буквами) - ')))
	print(a)