class AddStrings():
	def __init__(self):
		pass
	def does_adding(self, path):
		with open(path, 'r') as foo_file:
			f = foo_file.readlines()
		a = []
		b = []
		for i in f:
			if i[:-1] == '# questions':
				continue
			elif i[:-1] == '# true_answers':
				break
			a.append(i[:-1])
		
		for i in f[len(a):]:
			if i[:-1] == '# true_answers':
				continue
			else:
				b.append(i[:-1])
		if len(a) == 0:
			return 'zero'		
		if len(a) < 10:
			return 'short'
		elif len(a) == len(b):
			return (a[:-1], b[1:])
		else:
			return None
		
if __name__ == '__main__':
	s = AddStrings()
	#p = s.does_adding('/storage/emulated/0/Zybrila/Технический английский.zybr')
	p = s.does_adding('/storage/emulated/0/Zybrila/1.zybr')
	print(p)
	
	'''Импорт:
		
		from ReadFile import AddStrings'''
	
	'''Использование:
		
		AddStrings().does_adding('путь и файл')'''