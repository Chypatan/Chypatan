import os
from pathlib import Path

from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import sp, dp
from kivy.core.window import Window

class LongTouchButton(MDRectangleFlatIconButton, TouchBehavior):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.name_record = self.text #
		self.icon_record = self.icon
		self.duration_long_touch = .5
		self.pos_hint = {"center_x": .5, "center_y": .5}
		#self.line_color= 1, 0, 1, 1
		self.icon_color = (.5, .5, .5, 1)

	def on_long_touch(self, touch, *args):
		self.icon = 'delete'
		self.icon_color = (1, 0, 0, .8)

	def on_double_tap_(self, *args):
		self.icon = self.icon_record
		self.icon_color = (.5, .5, .5, 1)



if __name__ == '__main__':
	
	class SearchFiles:
		def __init__(self, path='/storage/emulated/0/Zybrila'):
			self.path = path
		
		def search(self, extension, word=''):
			number = 1
			a = []
			for root, dirs, files in os.walk(self.path):
				for i in files:
					if i.endswith(extension):
						if i.find(word) != -1:
							a.append(i)
							number += 1
			return a


	class MainApp(MDApp):
		def build(self):
			self.theme_cls.theme_style = "Light"
			self.box=MDBoxLayout(
				orientation = 'vertical',
				padding=dp(150), spacing=dp(10))
			list = SearchFiles().search('.t')
			for i in list:
				self.b = LongTouchButton(
					text=i[:-2],
					icon='script-text-outline')
				self.b.bind(on_release=self.any_action)
				self.b.bind(icon=self.change_beh)
				self.box.add_widget(self.b)
			self.d = MDRaisedButton(
				text='Удалить кнопки',
				on_press=self.deleter,
				pos_hint={'center_x':.5, 'center_y':.5},
				md_bg_color=(1, 0, 0, 1))
			self.box.add_widget(self.d)
			self.box.add_widget(MDRaisedButton(
				text='Создать',
				on_press=self.creater, 
				pos_hint={'center_x':.5, 'center_y':.5},
				md_bg_color=(0, 1, 0, 1)))
			return self.box

		def deleter(self, args):
			del_list = []
			for i in self.box.children:
				try:
					if i.icon == 'delete':
						del_list.append(i)
				except AttributeError:
					continue
			for i in del_list:
				self.box.remove_widget(i)
				os.remove('/storage/emulated/0/Zybrila/' + str(i.name_record)+'.t')

		def creater(self, args):
			for i in range(1, 9):
				open(f'/storage/emulated/0/Zybrila/кнопка {i}' + '.t', 'w')
				
		def ret_list(self):
			list_child = []
			for i in self.box.children:
				try:
					if i.icon:
						list_child.append(i.icon)
				except AttributeError: continue
			self.list_child=list_child
			return self.list_child

		def change_beh(self, args, iconi):
			if self.ret_list().count('delete') != 0:
				[i.unbind(on_release=self.any_action) for i in self.box.children]
				#[i.bind(on_release=self.qwerty) for i in self.box.children]
				#[i.unbind(icon=self.change_beh) for i in self.box.children]
				#self.d.md_bg_color=(1, 1, 0, 1)
			else:
				[i.bind(on_release=self.any_action) for i in self.box.children]
				[i.unbind(on_release=self.qwerty) for i in self.box.children]
			args.bind(on_press=self.re_bind)
			args.unbind(on_release=self.any_action)

		def qwerty(self, args):
			args.icon = 'delete'
			args.icon_color = (1, 0, 0, .8)
			args.unbind(on_release=self.qwerty)
			args.bind(on_press=self.re_bind)

		def re_bind(self, args):
			args.icon = args.icon_record
			args.icon_color = (.5, .5, .5, 1)
			args.unbind(on_press=self.re_bind)
			args.bind(on_release=self.iop)

		def iop(self, args):
			args.bind(on_release=self.any_action)

		def any_action(self, args):
			if args.icon == 'delete':
				pass
			else:
				args.text = args.state #'нажата'

	MainApp().run()