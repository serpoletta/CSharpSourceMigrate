#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import os
import json

dir = '/home/rita/Programs/PycharmProjects/CSharpMigrate/testdir'
finaldir = 'migrated/'

file = dir + '/test.cs'
diffs_path = dir + '/diffs.json'

''' Вспомогательные функции '''
# Проверяет, является ли файл .cs.
def is_cs_file(path):
	file_extension = '.cs'
	test = path.rfind(file_extension)
	return not (test==-1)


# Собирает список .cs-файлов директории рекурсивно.
def get_cs_files_list(path):
	files_list = []
	for file in os.listdir(path):
		cur_path = os.path.join(path, file)
		if is_cs_file(cur_path):
			files_list.append(cur_path)
		elif os.path.isdir(cur_path):
			files_list += get_cs_files_list(cur_path)
	return files_list

''' Класс, работающий с diff-моделью '''


class DiffAnalyzer:
	def __init__(self, diffs_path):
		with open(diffs_path) as f_diffs:
			parsed_diffs = json.loads(f_diffs.read())

		# Адреса в модели, по которым находятся отредактированные элементы
		self.addresses = {'signatureDiff':'oldName',
						 'initializationDiff':'methodName',
						 'scopeDiff':'methodName',
						 'namespaceDiff': 'methodClass',
						 'symanticDiff': 'methodName'}

		# Словарь комментариев по модели
		self.comments_text = {'signatureDiff':
								  'Необходимо изменить имя метода. Старое имя: %s, новое имя: %s',
							 'initializationDiff':'Изменены параметры инициализации. %s %s %s',
							 'scopeDiff':'Изменена область видимости',
							 'namespaceDiff': 'Измененена принадлежность классу',
							 'symanticDiff': 'Изменена семантика метода %s'}

		# Заполняем список измененных элементов по diff-модели
		self.edited = []
		self.helper = {}
		for elem in parsed_diffs:
			type_key = list(elem.keys())[0]
			name_key = self.addresses.get(type_key)
			new_edited = elem.get(type_key).get(name_key)
			if new_edited:
				self.edited.append(new_edited)
				self.helper[new_edited] = elem
		print(self.edited)
		print(self.helper)

	# Проверяет, содержится ли часть строки в diff-ах
	def contains(self, line):
		# Содержатся ли измененные наименования в строке
		for substr in self.edited:
			if not (line.rfind(substr)==-1):
				return True
		return False

	# Возвращает комментарий для текущей строки
	def comment(self, line):
		for substr in list(self.helper.keys()):
			if not (line.rfind(substr)==-1):
				# Взять данные
				# TODO: уточнить порядок аргументов
				data = tuple(list(self.helper[substr].values())[0].values())
				print(data)
				# Подставить в текст по ключу
				diff_type = list(self.helper[substr].keys())[0]
				text = str(self.comments_text.get(diff_type)) % data
				print(text)
				return '/*' + text + '*/' + '\n'
		return '/* Что-то изменилось */' + '\n'

''' Основная программа '''

# Миграция одного файла на основе diff-ов
def migrate(file, diffs):
	with open(file) as f_in, open(file.replace(dir, finaldir), 'w') as f_out:
		for line in f_in:
			if diffs.contains(line):
				comment = diffs.comment(line)
				f_out.write(comment)
			f_out.write(line)


def __main__():
	os.makedirs(finaldir, mode=0o777, exist_ok=True)
	diffs = DiffAnalyzer(diffs_path)
	for file in get_cs_files_list(dir):
		migrate(file, diffs)
		print('File ' + file + ' migrated')

#TODO: API

__main__()

