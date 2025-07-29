
from django import forms
from steps.models import Step





class StepBaseForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = ('target_goal',)
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Step description...', 'class': 'step-title-input'}
            ),
            'completed': forms.CheckboxInput(attrs={'class': 'step-completed-checkbox'})
        }





class StepCreateForm(StepBaseForm):
    ...


class StepEditForm(StepBaseForm):
    ...


class StepDeleteForm(StepBaseForm):
    ...