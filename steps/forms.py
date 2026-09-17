
from django import forms
from steps.models import Step





class StepBaseForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Step description...', 'class': 'step-title-input'}
            )
        }





class StepCreateForm(StepBaseForm):
    ...

class StepEditForm(StepBaseForm):
    ...


class StepDeleteForm(StepBaseForm):
    ...