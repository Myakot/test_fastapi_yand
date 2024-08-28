# Get a token to authorize
curl -X POST \
  http://0.0.0.0:8000/token \
  -d "username=your_username&password=your_password"

# Get a list of notes
curl -X GET \
  http://0.0.0.0:8000/notes \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json'

# Add a new note
curl -X POST \
  http://0.0.0.0:8000/notes \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"title": "New note", "content": "Note texxt"}'

# Get the note
curl -X GET \
  http://0.0.0.0:8000/notes/1 \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json'

# Update the note
curl -X PUT \
  http://0.0.0.0:8000/notes/1 \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated Note", "content": "This is an updated note"}'

# Delete the note
curl -X DELETE \
  http://0.0.0.0:8000/notes/1 \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json'

# Delete all notes
curl -X DELETE \
  http://0.0.0.0:8000/notes/ \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json'