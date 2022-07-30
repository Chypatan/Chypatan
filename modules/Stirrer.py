import random

class ListShuffle:
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		
	def shuffle(self, questions, answers):
		self.shuffle_list = []
		
		for i in range(len(questions)):
			self.shuffle_list.append(i)
			
		random.shuffle(self.shuffle_list)
		
		global a
		a = []
		global b
		b = []
		
		for i in self.shuffle_list:
			a.append(questions[i])
			b.append(answers[i])
			
	def quest(self):
		return a
	def ans(self):
		return b
			

if __name__=='__main__':
	
	questions = ['huge', 'composable', 'recycle', 'persistent', 'translucent', 'accent', 'whole', 'template', 'describe', 'constitutes', 'source', 'same', 'convention', 'humidity', 'proximity']
		
	true_answers = ['огромный', 'компонуемый', 'перерабатывать', 'настойчивый', 'полупрозрачный', 'акцент', 'весь', 'шаблон', 'описывать', 'составляет', 'источник', 'такой же', 'соглашение', 'влажность', 'близость']
	
	ListShuffle().shuffle(questions, true_answers)
	print(ListShuffle().quest())
	print(ListShuffle().ans())