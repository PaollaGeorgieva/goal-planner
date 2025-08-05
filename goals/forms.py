from django import forms


from goals.mixins import CategoryMixin
from goals.models import TargetGoal, HabitGoal, Category

class GoalBaseForm(CategoryMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="–– Choose Category ––"
    )
    new_category = forms.CharField(
        required=False,
        label="New Category",
        widget=forms.TextInput(attrs={'placeholder': 'If not in the list'}))

    class Meta:
        model = None
        fields = ['goal_type', 'title', 'description', 'start_date', 'category', 'new_category']
        widgets = {
            'goal_type': forms.RadioSelect(attrs={"class": "goal-type-radio"}),
            'title': forms.TextInput(attrs={'placeholder': 'Your goal...', 'id': 'id_title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Add details...', 'id': 'id_description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_start_date'}),
        }




class TargetGoalCreateForm(GoalBaseForm):

    class Meta(GoalBaseForm.Meta):
        model = TargetGoal
        fields = GoalBaseForm.Meta.fields + ["end_date"]
        widgets = {
            **GoalBaseForm.Meta.widgets,
            "end_date": forms.DateInput(attrs={"type": "date", "id": "id_end_date"}),
        }
        widgets["goal_type"].choices = TargetGoal.TYPE_CHOICES





class TargetGoalUpdateForm(TargetGoalCreateForm):
    class Meta(TargetGoalCreateForm.Meta):

        fields = [ 'title', 'description', 'start_date', 'end_date']

class TargetGoalDeleteForm(TargetGoalCreateForm):
    ...

class HabitGoalCreateForm(GoalBaseForm):
    class Meta(GoalBaseForm.Meta):
        model = HabitGoal
        fields = GoalBaseForm.Meta.fields + ["target_per_period", "period_unit"]
        widgets = {
            **GoalBaseForm.Meta.widgets,
            "target_per_period": forms.NumberInput(attrs={"min": 1, "value": 1, "id": "id_target_per_period"}),
            "period_unit": forms.RadioSelect(choices=HabitGoal.PERIOD_CHOICES),
        }
        widgets["goal_type"].choices = HabitGoal.TYPE_CHOICES





class HabitGoalUpdateForm(HabitGoalCreateForm):
    class Meta(HabitGoalCreateForm.Meta):
        fields = \
            [
             'title',
             'description',
             'start_date',
             'target_per_period',
             'period_unit',
             'category',
             'new_category']


class HabitGoalDeleteForm(HabitGoalCreateForm):
    ...


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for goals...',
                'class': 'my-search-input',
                'autocomplete': 'off',
            }
        )
    )