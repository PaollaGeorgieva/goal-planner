from django import forms
from notes.models import Note

class NoteBaseForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('content_type', 'object_id')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Note title...',
                'class': 'step-title-input'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'class': 'note-content-textarea',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'note-image-upload'
            })
        }


class NoteCreateForm(NoteBaseForm):
    pass


class NoteEditForm(NoteBaseForm):
    pass


class NoteDeleteForm(NoteBaseForm):
    ...
