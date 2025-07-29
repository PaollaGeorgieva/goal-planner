from django import forms
from django.db import models

from .mixins import CategoryMixin
from .models import TargetGoal, HabitGoal, Category


class TargetGoalBaseForm(CategoryMixin,forms.ModelForm):
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
        model = TargetGoal
        fields = ['goal_type', 'title', 'description', 'start_date', 'end_date', 'category',             'new_category' ]
        widgets = {
            'goal_type': forms.RadioSelect(choices=TargetGoal.TYPE_CHOICES, attrs={'class': 'goal-type-radio'}),
            'title': forms.TextInput(attrs={'placeholder': 'Your goal...', 'id': 'id_title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Add details...', 'id': 'id_description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_start_date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_end_date'}),
        }



class TargetGoalCreateForm(TargetGoalBaseForm):
    ...

class TargetGoalUpdateForm(TargetGoalBaseForm):
    class Meta(TargetGoalBaseForm.Meta):

        fields = [ 'title', 'description', 'start_date', 'end_date']

class TargetGoalDeleteForm(TargetGoalBaseForm):
    ...

class HabitGoalBaseForm(CategoryMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="–– Choose Category ––"
    )
    new_category = forms.CharField(
        required=False,
        label="New Category",
        widget=forms.TextInput(attrs={'placeholder': 'If not in the list'})
    )
    class Meta:
        model = HabitGoal
        fields =\
            ['goal_type',
             'title',
             'description',
             'start_date',
             'target_per_period',
             'period_unit',
             'category',
             'new_category']
        widgets = {
            'goal_type': forms.RadioSelect(choices=HabitGoal.TYPE_CHOICES, attrs={'class': 'goal-type-radio'}),
            'title': forms.TextInput(attrs={'placeholder': 'Your goal...', 'id': 'id_title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Add details...', 'id': 'id_description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_start_date'}),
            'target_per_period': forms.NumberInput(attrs={'min': 1, 'value': 1, 'id': 'id_target_per_period'}),
            'period_unit': forms.RadioSelect(choices=HabitGoal.PERIOD_CHOICES),
        }



class HabitGoalCreateForm(HabitGoalBaseForm):
    ...


class HabitGoalUpdateForm(HabitGoalBaseForm):
    class Meta(HabitGoalBaseForm.Meta):
        fields = \
            [
             'title',
             'description',
             'start_date',
             'target_per_period',
             'period_unit',
             'category',
             'new_category']


class HabitGoalDeleteForm(HabitGoalBaseForm):
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