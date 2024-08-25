# Получить список заметок
curl -X GET \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json'

# Создать новую заметку
curl -X POST \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title": "Новая заметка", "content": "Текст заметки"}'
