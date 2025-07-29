from django.urls import path
from notes.views import GoalNotesView, CreateNoteView, EditNoteView, NoteDeleteView

app_name = 'notes'

urlpatterns = [
    path('', GoalNotesView.as_view(), name='goal-notes'),
    path('add/', CreateNoteView.as_view(), name='add-note'),
    path('<int:note_id>/edit/', EditNoteView.as_view(), name='edit-note'),
    path('<int:note_id>/delete', NoteDeleteView.as_view(), name='delete-note')
]