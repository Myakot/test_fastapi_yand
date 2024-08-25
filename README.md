# Задача

Необходимо спроектировать и реализовать на Python сервис,
предоставляющий REST API интерфейс с методами:
- добавление заметки
- вывод списка заметок

Данные необходимо хранить либо в текстовом файле (в формате json, либо csv),
либо в базе данных (PostreSQL или MongoDB).

При сохранении заметок необходимо орфографические ошибки валидировать при помощи сервиса Яндекс.Спеллер https://yandex.ru/dev/speller/
Также необходимо реализовать аутентификацию и авторизацию. Пользователи должны иметь доступ только к своим заметкам.
Возможность регистрации не обязательна, допустимо иметь предустановленный набор пользователей (механизм хранения учетных записей любой, вплоть до hardcode в приложении.)
### Условия
- Для реализации сервиса использовать Python
- Сервис должен работать через REST API, передавать данные в формате json
- Для реализации web-сервера использовать любой асинхронный веб-фреймворк (aiohttp, fastapi)
- В коде должны корректно быть представлены type hint'ы
- Использовать средства автоматизированного форматирования исходного кода (yapf или black)
- Запуск сервиса и требуемой им инфраструктуры должен производиться в докер контейнерах
- Желательно продумать удобство проверки работоспособности методов API при ревью задачи (шаблоны curl запросов, postman коллекция, тесты и т.п.)

Пожелания:
Использовать максимально простые решения, главное оформлять их стилистически и архитектурно правильно.
