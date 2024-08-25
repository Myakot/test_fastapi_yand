# Получить список заметок
curl -X GET \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json'

# Создать новую заметку
curl -X POST \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title": "Новая заметка", "content": "Текст заметки"}'

# Получить конкретную заметку
curl -X GET \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json'

# Обновить конкретную заметку
curl -X PUT \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated Note", "content": "This is an updated note"}'

# Обновить заметку в пустую
curl -X PUT \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"title": "", "content": ""}'

# Удалить конкретную заметку
curl -X DELETE \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json'

# Удалить все заметки
curl -X DELETE \
  http://localhost:8000/notes/ \
  -H 'Content-Type: application/json'
