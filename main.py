#  -*-  coding: utf-8 -*-
__version__ = '1.0'
import textwrap
import random
import shutil
import math
import sys
import os

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.toast import toast
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from modules.ReadFile import AddStrings
from modules.Stirrer import ListShuffle as LS
from modules.SearchFiles import SearchFiles
from modules.buttons.MyLongTouchButton import LongTouchButton

# Здесь приложение запрашивает у системы доступ к памяти
if platform == 'android':
	from android.permissions import request_permissions, Permission
	request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
	from android.storage import primary_external_storage_path

class Enter(MDScreen):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.ids.Toolbar.left_action_items=[["menu", lambda x: Clock.schedule_once(self.switcher)]]
		self.ids.Toolbar.right_action_items=[['file-plus-outline', lambda x: Clock.schedule_once(self.add)], ['exit-to-app', lambda x: Clock.schedule_once(self.exit_), 'выход']]
		self.count = 0
		self.ans_true = 0
		self.ids.Question.bind(on_touch_move=lambda x, touch: self.gesture_open(touch))
		Window.bind(on_keyboard=self.key_input)
		
	def file_selection(self, args):
		if args.icon == 'delete' :
			pass
		else:
			# qa получает список с двумя вложенными списками
			qa = AddStrings().does_adding(f'/storage/emulated/0/Zybrila/{args.text}.zybr')
			if qa is None:
				toast('Файл составлен неверно', True, 80, 500, 0)
			elif qa == 'short':
				toast('Слишком короткое содержимое', True, 80, 500, 0)
			elif qa == 'zero':
				toast('Файл абсолютно пуст',
					True, 80, 500, 0)
			else:
				# получаем список вопросов
				self.questions = qa[0]
				# получаем список ответов
				self.true_answers = qa[1]
				Clock.schedule_once(self.shuffler)
				self.ids.Toolbar.title = args.text
				Clock.schedule_once(self.options_back)
			# создаётся список с блоками ответов
			self.answers = []
			# создаются счётчики вопросов и правильных ответов на них
			self.count = 0
			self.ans_true = 0
			
	def shuffler(self, args):
		# списки вопросов и ответов перемешиваются в случайной последовательности, но соответствуют друг другу
		LS().shuffle(self.questions,
							self.true_answers)
		Clock.schedule_once(self.doing)

	# процесс прохождения теста
	def doing(self, args):
		self.questions = LS().quest()
		self.true_answers = LS().ans()
		# создаются блоки ответов на вопросы
		for i in self.true_answers:
			self.ans = []
			# добавляется один правильный ответ
			self.ans.append(i)
			# добавляется 3 неправильных ответа
			while len(self.ans) < 4:
				lie_ans = random.choice(
							self.true_answers)
				self.ans.append(lie_ans)
				# исключаются повторения с помощью метода set
				self.ans = list(set(self.ans))
			self.answers.append(self.ans)
		# проверка существования виджетов с ответами и их удаление
		try:
			self.ids.place_for_buttons.clear_widgets()
			self.ids.Basic.remove_widget(self.shield)
		except: pass
		if self.count == len(self.questions):
			Clock.schedule_once(self.itog)
			self.ids.Counter_questions.text = ''
		else:
			self.ids.Question.text = textwrap.fill(str(self.questions[self.count]), 28)
			random.shuffle(self.answers[self.count])
			self.ids.Counter_questions.text=f'{self.count+1} вопрос из {len(self.questions)}'
			# создание кнопок с вариантами ответов
			for answer in self.answers[self.count]:
				variants_btns = Factory.VariantsButtons()
				variants_btns.bind(
					on_release=self.examination)
				variants_btns.text = str(answer)
				self.ids.place_for_buttons.add_widget(variants_btns)
				self.variants_btns = variants_btns
		self.count +=1

	# проверка истинности ответа
	def examination(self, args):
		if args.text == str(self.true_answers[self.count - 1]):
			args.md_bg_color = [.5, .7, 0, 1]
			self.ans_true +=1
			toast(
					'Правильно',
					True, 80, 500, 0)
		else:
			args.md_bg_color = [1, 0, 0, 1]
			toast(
				str(self.true_answers[self.count - 1]),
				True, 80, 500, 0)
		'''ставится экран для защиты от
		нажатия, пока идёт проверка, что
		бы избежать неправильной
		работы приложения из-за
		невыдержанных таймингов
		между вопросами'''
		self.shield = Factory.Shield()
		self.ids.Basic.add_widget(self.shield)
		Clock.schedule_once(self.doing, 1.5)

	# оценка результатов прохождения теста
	def itog(self, args):
		self.ids.Question.text = f'Правильных ответов: {self.ans_true} из {self.count - 1}'
		refresh = Factory.VariantsButtons()
		refresh.bind(on_press=self.reset)
		refresh.text = 'Ещё раз?'
		self.ids.place_for_buttons.add_widget(refresh, index = 5)
		percent_true = math.ceil(100 / len(self.questions) * self.ans_true)
		if percent_true <= 60:
			grade = 'Плохо'
		elif 61 < percent_true <= 80:
			grade = 'Неплохо'
		elif 81 < percent_true <= 95:
			grade = 'Хорошо'
		else:
			grade = 'Отлично'
		self.ids.Counter_questions.text = f'{grade}. Правильных ответов {percent_true}%'

	def reset(self, args):
		self.count = 0
		self.ans_true = 0
		self.ids.place_for_buttons.clear_widgets()
		Clock.schedule_once(self.doing)

	# жест пальцем по экрану
	def gesture_open(self, touch):
		'''определяется расстояние для
		жеста. В данном случае это левая
		половина экрана'''
		if touch.sx < .5:
		  '''определяется скорость жеста с
		  помощью дельты координат по
		  оси Х'''
		  if touch.dx > 10:
		  	Clock.schedule_once(self.switcher)

	'''переключатель движения бокового
	меню. Если оно открыто, то
	закроется, и наоборот'''
	def switcher(self, args):
		try:
			self.opt
			Clock.schedule_once(self.options_back)
		except:
			Clock.schedule_once(self.options)

	def options(self, args):
		try:
			os.mkdir('/storage/emulated/0/Zybrila')
			shutil.copy('./Advanced english.zybr', '/storage/emulated/0/Zybrila', follow_symlinks=True)
			shutil.copy('./Simple english.zybr', '/storage/emulated/0/Zybrila', follow_symlinks=True)
			os.rename('/storage/emulated/0/Zybrila/Advanced english.zybr', '/storage/emulated/0/Zybrila/Технический английский.zybr')
			os.rename('/storage/emulated/0/Zybrila/Simple english.zybr', '/storage/emulated/0/Zybrila/Школа второй класс.zybr')
		except FileExistsError:
			pass
		self.opt = Factory.ListBackground()
		self.opt.ids.plm.bind(on_press=self.options_back)
		self.opt.ids.Constructor.bind(on_press=self.add)
		self.ids.Basic.add_widget(self.opt)
		self.move=Animation(
			pos_hint={'center_x':.45, 'center_y':.46},
			duration=.17)
		self.move.start((self.opt))
		list_items = SearchFiles('/storage/emulated/0/Zybrila').search('zybr', '')
		list_items = sorted(list_items)
		for i in list_items:
			self.asd = LongTouchButton(
					text=i[:-5],
					icon='script-text-outline')
			self.asd.bind(on_release=self.file_selection)
			self.asd.bind(icon=self.change_begavior_const)
			self.opt.ids.Greed.add_widget(self.asd)

	def options_back(self, args):
		self.move_back = Animation(
			pos_hint= {'center_x':-1, 'center_y':.46},
			duration=.17)
		self.move_back.start(self.opt)
		del self.opt

	def options_close(self, args):
		if args.icon == 'delete':
			pass
		else:
			self.move_back = Animation(
				pos_hint= {'center_x':-1, 'center_y':.46},
				duration=.17)
			self.move_back.start(self.opt)
			del self.opt

	# изменение поведения кнопок списка при их нажатии
	def change_begavior_const(self, button, args):
		# проверка, есть ли хоть один выделенный элемент списка
		L = []
		for i in self.opt.ids.Greed.children:
			try:
				if i.icon:
					L.append(i.icon)
			except AttributeError: pass
		if L.count('delete') != 0:
			self.opt.ids.Constructor.text = 'Удалить'
			self.opt.ids.Constructor.md_bg_color = (1, 0, 0, .8)
			self.opt.ids.Constructor.unbind(
				on_press=self.add) # tyt
			self.opt.ids.Constructor.bind(on_press=self.delete_rec)
		else:
			self.opt.ids.Constructor.text = 'Конструктор'
			self.opt.ids.Constructor.md_bg_color = (0, .5, 0, .9)
			self.opt.ids.Constructor.unbind(
				on_press=self.delete_rec)
			self.opt.ids.Constructor.bind(
				on_press=self.add) # tyt
		button.bind(on_press=self.rebind)
		button.unbind(on_release=self.file_selection)

	#перепривязка кнопок
	def rebind(self, args):
		args.icon = args.icon_record
		args.icon_color = (.5, .5, .5, 1)
		args.unbind(on_press=self.rebind)
		args.bind(on_release=self.auxiliary_bind)

	def auxiliary_bind(self, args):
		'''если сделать эту привязку кнопки
		в предыдущем методе, а не
		здесь, то файл будет открываться
		даже если он помечен для
		удаления'''
		args.bind(on_release=self.file_selection)

	def delete_rec(self, args):
		list_rec = []
		for i in self.opt.ids.Greed.children:
			try:
				if i.icon == 'delete':
					list_rec.append(i)
			except AttributeError:
				continue
		for i in list_rec:
			self.opt.ids.Greed.remove_widget(i)
			os.remove(
				'/storage/emulated/0/Zybrila/'
				+ str(i.text)
				+ '.zybr')
		self.opt.ids.Constructor.text = 'Конструктор'
		self.opt.ids.Constructor.md_bg_color = (0, .5, 0, .9)
		self.opt.ids.Constructor.unbind(
				on_press=self.delete_rec)
		self.opt.ids.Constructor.bind(
				on_press=self.add) # tyt

	def add(self, args):
		self.manager.current = '2'
		self.manager.transition.direction = 'left'

	def exit_(self, args):
		sys.exit()

	# отслеживает нажатия кн. "назад"
	def key_input(self, window,
							key, scancode,
							codepoint, modifier):
		try:
			if key == 27:
				for i in self.opt.ids.Greed.children:
					try:
						if i.icon:
							i.icon = i.icon_record
							i.icon_color = (.5, .5, .5, 1)
					except AttributeError:
						pass
			else:
				return False
		except AttributeError:
			toast('Нажмите значок выхода',
					True, 80, 500, 0)





class Creator(MDScreen):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.count = 1
		count=self.count
		self.ids.q.helper_text = f'Вопрос № {self.count}'
		self.ids.save.disabled = True
		self.list_of_questions = []
		self.list_of_answers = []

	def counter(self):
		self.count += 1
		self.ids.q.helper_text = f'Вопрос № {self.count}'
		if self.count>10:
			self.ids.save.disabled = False
		self.list_of_questions.append(self.ids.q.text)
		self.list_of_answers.append(self.ids.a.text)
		self.ids.q.text = ''
		self.ids.a.text = ''

	def zero_counter(self):
		self.count = 1
		self.ids.q.helper_text = f'Вопрос № {self.count}'
		self.ids.save.disabled = True
		self.ids.n.text = ''

	def save_list(self):
		if self.ids.n.text not in ('', ' '):
			name=self.ids.n.text
			f=open(f'/storage/emulated/0/Zybrila/{name}.zybr', 'w')
			f.write('# questions'+'\n')
			f.close()
			with open(f'/storage/emulated/0/Zybrila/{name}.zybr', 'a') as f:
				for i in range(len(self.list_of_questions)):
					f.write(str(self.list_of_questions[i])+'\n')

			with open(f'/storage/emulated/0/Zybrila/{name}.zybr', 'a') as f:
				f.write('\n# true_answers'+'\n')
				for i in range(len(self.list_of_answers)):
					f.write(str(self.list_of_answers[i])+'\n')
			self.manager.current = '1'
			self.zero_counter()
		else:
			self.warning=MDDialog(
				title='Внимание!',
				auto_dismiss=False,
				type='alert',
				text='Заполните поле "Название", что бы создать тест.',
				buttons=[MDFlatButton(
					text='Ладно',
					on_press=self.dialod_dismiss)])
			self.warning.open()

	def dialod_dismiss(self, args):
		self.warning.dismiss()
		Clock.schedule_once(self.focus_name, .2)
	def focus_name(self, args):
		self.ids.n.focus = True





class MyApp(MDApp):
	def build(self):
		Window.bind(
			on_keyboard=self.key_input)
		#return Enter()
		self.sm = ScreenManager()
		self.sm.add_widget(Enter(name='1'))
		self.sm.add_widget(Creator(name='2'))
		#self.sm.current = '2'
		return self.sm
		
	def on_start_(self):
		self.fps_monitor_start()
		
	def key_input(self, window,
							key, scancode,
							codepoint, modifier):
		if key == 27:
			#toast('Нажмите ещё раз для выхода', True, 80, 500, 0)
			return True
		else:
			return False

	def on_pause(self):
		toast('Приложение приостановлено',
				True, 80, 500, 0)
		return True
	
	def on_resume(self):
		toast('Приложение работает',
				True, 80, 500, 0)
		return True
		
if __name__ == '__main__':
	MyApp().run()