#!/usr/bin/python
# -*- coding: utf-8 -*-

# Перенос задач из Redmine в Битрикс24

# 1. Регистрируем приложение в битриксе. 
# Заходим в меню Мои приложения - Добавить приложение.
# Задаем название. Например “Redmine2Bitrix24”.
# Устанавливаем флаг “Приложение использует только API”.
# Устанавливаем права доступа на “Задачи (task)” и “Задачи (расширенные права) (tasks_extended)”.
# В пункте “Укажите ссылку*” я указал ссылку на Redmine в локальной сети. http://_IP_REDMINESERVER_
# Сохраняем и получаем код и ключ приложения: 
# Код приложения: local.xxxxxxxxxxxxxxxx.xxxxxxxxxxx
# Ключ приложения:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 2. Заходим на адрес битрикса, подставив в client_id полученный на предыдущем шаге код приложения.
# https://_ВАШ_БИТРИКС_.bitrix24.ru/oauth/authorize/?client_id=_КОД_ПРИЛОЖЕНИЯ_

# Сервер перенаправит нас на сервер redmine (ссылку мы указали при регистрации приложения) и мы получи ссылку:
# http://_IP_REDMINESERVER_/?code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy&server_domain=oauth.bitrix.info

# из полученной ссылки нам нужен параметр
# code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Внимение! Полученный код действителен в течение 30 сек!

# 3. Сформируем ссылку для запроса кода авторизации и перейдем по ней

# https://oauth.bitrix.info/oauth/token/?grant_type=authorization_code&client_id=_КОД_ПРИЛОЖЕНИЯ_ИЗ П1_&client_secret=_КЛЮЧ_ПРИЛОЖЕНИЯ_ИЗ_П1&code=_КОД_ИЗ П2

# в итоге получить ответ, из которого взять access_token.

# {

#      "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#      "expires_in": 3600,
#      "scope": "app",
#      "domain": "oauth.bitrix.info",
#      "server_endpoint": "https://oauth.bitrix.info/rest/",
#      "status": "L",
#      "client_endpoint": "https://_ВАШ_БИТРИКС_.bitrix24.ru/rest/",
#      "member_id": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
#      "refresh_token": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"

# }

# Полученный access_token подставить в переменную auth

import requests

# По хорошему это надо в цикл
# 1. Перенос открытых задач.
#	Redmine отдает максимум по 100 задач за вызов, поэтому переносим порциями, используя параметр offset

# 1.1 Первые 0-100 задач
rj = requests.get('http://_IP_REDMINESERVER_/issues.json?offset=0&limit=100').json()

# 1.2 Следующие 100-200 задач
# rj = requests.get('http://_IP_REDMINESERVER_/issues.json?offset=100&limit=100').json()
#	1.3  и т.д.

# 2. Для перенос закрытых задач добавить параметр status_id=closed и раскомментивароть строки заполнения полей "Статус" и "Плановая дата завершения"
# rj = requests.get('http://_IP_REDMINESERVER_/issues.json?status_id=closed&offset=410&limit=100').json()

for i in rj["issues"]:
	print i["id"]
	print i["subject"]
	
	# Заголовок задачи
	title = i["subject"]

	# Описание задачи
	if "description" in i:
		description = i["description"] + " id_redmine: " + str(i["id"])
	else:
		description = "id_redmine: " + str(i["id"])

	# Ответственный за задачу
	if "assigned_to" in i:
		if i["assigned_to"]["id"] == 9: # ID ответственного в Redmine
			# ИД ответственного в битриксе. Можно посмотреть в адресной строке, залогинившись и перейти в пункт "Моя страница".
			# https://zzz.bitrix24.ru/company/personal/user/4/
			responsible_id = "1"
		else:
			responsible_id = "4"
	else:
		responsible_id = "4"

	# Автор задачи
	if i["author"]["id"] == 9:
		created_by = "1"
	else:
		created_by = "4"

	# Битрикс не даёт записывать поля "Дата начала" и "Дата завершения" задачи, поэтому использовал поля "Плановая дата начала" и "Плановая дата завершения".
	start_date_plan = i["created_on"]

	# 2.1 Раскомментировать строки ниже для переноса закрытых задач. Статус задачи = Закрыта. Плановая дата завершения = Дата завершения из Redmine
	# status = "5"
	# end_date_plan = i["closed_on"];

	# Вместо _ВАШ_access_token_ подставить полученный вами
	auth = "_ВАШ_access_token_"

	url = "https://_ВАШ_БИТРИКС_.bitrix24.ru/rest/task.item.add.json?auth={0}".format(auth)
	url = url + "&arParams[TITLE]=" + title
	url = url + "&arParams[RESPONSIBLE_ID]=" + responsible_id
	url = url + "&arParams[DESCRIPTION]=" + description
	url = url + "&arParams[CREATED_BY]=" + created_by
	
	# 2.2 Раскомментировать 2 строки ниже для перенос закрытых задач
	# url = url + "&arParams[STATUS]=" + status
	# url = url + "&arParams[END_DATE_PLAN]=" + end_date_plan

	r = requests.post(
	    url,
	    headers={
	        "Accept-Language": "ru",
	        "Accept-Charset": "utf-8",
	        "Content-Language": "ru",
	        "Content-Charset": "utf-8",
	        "Content-type": "application/json; charset=utf-8",
	    },
	)

	# Вывод номера созданной в битриксе задачи
	print r.text.decode("utf-8")