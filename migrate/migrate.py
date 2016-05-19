#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import os
import json
import socket

dir = '/home/rita/Programs/PycharmProjects/CSharpMigrate/testdir'
finaldir = 'migrated/'

file = dir + '/test.cs'

''' Вспомогательные функции '''

# Получает с сервера диффы
def get_diffs():
	reg_str = '{type: setModuleType, parameters: srcMigrate}'
	sock = socket.socket()
	sock.connect(('localhost', 9090))
	sock.send(reg_str.encode('utf-8'))

	data = sock.recv(1024*10).decode('utf-8')
	sock.close()
	return data

# Проверяет, является ли файл .cs.
def is_cs_file(path):
	file_extension = '.cs'
	test = path.rfind(file_extension)
	return not (test == -1)


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
	# Модель
	model = 		{'methodSignatureDiff':('oldName', 'newName', 'className', 'namespace'),
						 'methodInitializationDiff':('methodName', 'oldArgs', 'newArgs', 'className', 'namespace'),
						 'accessDiff': ('name', 'type', 'accessModif', 'namespace', 'class') ,
						 'namespaceDiff': ('className', 'oldNamespace', 'newNamespace'),
						 'methodSymanticDiff': ('name', 'className', 'namespace')}

	# Словарь комментариев по модели
	comments_text = 	{'methodSignatureDiff':
							  'Необходимо изменить имя метода. Старое имя: %s, новое имя: %s, '
							  'имя класса: %s, пространство имен: %s',
						 'methodInitializationDiff':
							 'Изменены параметры инициализации. Имя метода: '
							 '%s, старые аргументы: %s, новые аргументы: %s, имя класса: %s, пространство имен: %s',
						 'accessDiff':
								'Изменена область видимости. Имя: %s, тип: %s, '
								'модификатор доступа: %s, пространство имен: %s, класс: %s',
						 'namespaceDiff':
							'Измененено пространство имен. Имя класса: %s, старое '
							'пространство имен: %s, новое пространство имен: %s',
						 'methodSymanticDiff':
							'Изменена семантика. Имя: %s, имя класса: %s, пространство имен: %s'}

	def __init__(self, diffs):
		#with open(diffs_path) as f_diffs:
		#	parsed_diffs = json.loads(f_diffs.read())

		parsed_diffs = json.loads(self.to_real_json(diffs))

		# Заполняем список измененных элементов по diff-модели
		self.edited = []
		self.helper = {}
		for elem in parsed_diffs:
			type_key = list(elem.keys())[0]
			name_key = self.model.get(type_key)[0]
			new_edited = elem.get(type_key).get(name_key)
			if new_edited:
				self.edited.append(new_edited)
				self.helper[new_edited] = elem

	# Костыль для получаемого ненастоящего json-а
	def to_real_json(self, json_str):
		real_json_str = json_str
		model_list = list(self.model.keys())
		for elem in list(self.model.values()):
			model_list += (list(elem))
		for elem in model_list:
			real_json_str = real_json_str.replace(elem + ':', '"' + elem + '" :')
		return real_json_str.replace("'", '"').replace('[Object]','"[Object]"')

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
			if not (line.rfind(substr) == -1):
				# Взять данные
				substr_data = self.helper[substr]
				diff_type_name = list(substr_data.keys())[0]
				args = tuple(self.model.get(diff_type_name))
				data = []
				for arg in args:
					data.append(substr_data[diff_type_name][arg])

				# Подставить в текст по ключу
				text = str(self.comments_text.get(diff_type_name)) % tuple(data)
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
	diffs = DiffAnalyzer(get_diffs())
	for file in get_cs_files_list(dir):
		migrate(file, diffs)
		print('File ' + file + ' migrated')

__main__()

