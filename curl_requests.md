# Get a list of notes
curl -X GET \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json'

# Add a new note
curl -X POST \
  http://localhost:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title": "New note", "content": "Note text"}'

# Get the note
curl -X GET \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json'

# Update the note
curl -X PUT \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated Note", "content": "This is an updated note"}'

# Delete the note
curl -X DELETE \
  http://localhost:8000/notes/1 \
  -H 'Content-Type: application/json'

# Delete all notes
curl -X DELETE \
  http://localhost:8000/notes/ \
  -H 'Content-Type: application/json'
