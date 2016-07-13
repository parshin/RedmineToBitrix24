# RedmineToBitrix24
Impoirt tasks from Redmine to Bitrix24
Пример переноса задач из Redmine в Битрикс24 с помощью python скрипта.
В примере показан процесс авторизации и отправка полученных задач в Битрикс24.

Перенос задач из Redmine в Битрикс24

1. Регистрируем приложение в битриксе. 
Заходим в меню Мои приложения - Добавить приложение.
Задаем название. Например “Redmine2Bitrix24”.
Устанавливаем флаг “Приложение использует только API”.
Устанавливаем права доступа на “Задачи (task)” и “Задачи (расширенные права) (tasks_extended)”.
В пункте “Укажите ссылку*” я указал ссылку на Redmine в локальной сети. http://_IP_REDMINESERVER_
Сохраняем и получаем код и ключ приложения: 
Код приложения: local.xxxxxxxxxxxxxxxx.xxxxxxxxxxx
Ключ приложения:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

2. Заходим на адрес битрикса, подставив в client_id полученный на предыдущем шаге код приложения.
https://_ВАШ_БИТРИКС_.bitrix24.ru/oauth/authorize/?client_id=_КОД_ПРИЛОЖЕНИЯ_

Сервер перенаправит нас на сервер redmine (ссылку мы указали при регистрации приложения) и мы получи ссылку:
http://_IP_REDMINESERVER_/?code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy&server_domain=oauth.bitrix.info

из полученной ссылки нам нужен параметр
code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Внимение! Полученный код действителен в течение 30 сек!

3. Сформируем ссылку для запроса кода авторизации и перейдем по ней

https://oauth.bitrix.info/oauth/token/?grant_type=authorization_code&client_id=_КОД_ПРИЛОЖЕНИЯ_ИЗ П1_&client_secret=_КЛЮЧ_ПРИЛОЖЕНИЯ_ИЗ_П1&code=_КОД_ИЗ П2

в итоге получить ответ, из которого взять access_token.

{

     "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
     "expires_in": 3600,
     "scope": "app",
     "domain": "oauth.bitrix.info",
     "server_endpoint": "https://oauth.bitrix.info/rest/",
     "status": "L",
     "client_endpoint": "https://_ВАШ_БИТРИКС_.bitrix24.ru/rest/",
     "member_id": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
     "refresh_token": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"

}

Полученный access_token подставить в переменную auth python скрипта.
