
from itertools import chain
from operator import attrgetter



from goals.models import TargetGoal, HabitGoal, Category
from django.db.models import Q
from django.db import models

class GoalListMixin:
    def get_user(self):
        return self.request.user

    def get_all_user_goals(self, user=None):

        user = self.get_user()

        target_goals = TargetGoal.objects.filter(user=user)
        habit_goals = HabitGoal.objects.filter(user=user)

        return sorted(
            chain(target_goals, habit_goals),
            key=attrgetter('created_at'),
            reverse=True
        )

    def get_recent_goals(self, limit=4, user=None):

        all_goals = self.get_all_user_goals(user)
        return all_goals[:limit]

    def get_all_user_categories(self):

        user = self.get_user()
        return Category.objects.filter(
            Q(targetgoal__user=user) |
            Q(habitgoal__user=user)
        ).distinct().order_by('name')

    def get_filtered_user_goals(self, category=None):


        user = self.get_user()
        selected_category = category or self.request.GET.get('category')


        if selected_category == 'Completed':
            qs_target = TargetGoal.objects.filter(user=user, is_completed=True)
            qs_habit = HabitGoal.objects.filter(user=user, is_completed=True)

        else:

            base_filters = dict(user=user, is_completed=False)

            if selected_category and selected_category != 'All':
                try:
                    cat = Category.objects.get(name=selected_category)
                    base_filters['category'] = cat
                except Category.DoesNotExist:
                    return []

            qs_target = TargetGoal.objects.filter(**base_filters)
            qs_habit = HabitGoal.objects.filter(**base_filters)

        filtered_goals = sorted(
            chain(qs_target, qs_habit),
            key=attrgetter('created_at'),
            reverse=True
        )
        return filtered_goals



class CategoryMixin:


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['category'].queryset = self.get_filtered_categories(self.user)

        if self.instance.pk:
            self.fields['category'].initial = self.instance.category

    def get_filtered_categories(self, user):
        return Category.objects.filter(
            models.Q(is_system=True) | models.Q(created_by=user)
        ).order_by('-is_system', 'name')

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get('new_category')
        selected_category = cleaned_data.get('category')


        if new_category:
            if Category.objects.filter(name__iexact=new_category, is_system=True).exists():
                self.add_error('new_category', "This system category already exists")
            elif self.user and Category.objects.filter(name__iexact=new_category, created_by=self.user).exists():
                self.add_error('new_category', "You already created a category with this name")
            elif len(new_category) > 100:
                self.add_error('new_category', "Max 100 characters")


        if not selected_category and not new_category:
            self.add_error('category', "Select a category or create a new one")


        if selected_category and new_category:
            self.add_error('category', "You can't choose a category and create a new one at the same time.")
            self.add_error('new_category', "You can't create a new category if you've selected one from the list.")

        return cleaned_data



class GoalFormValidMixin:
    def form_valid(self, form):
        goal = form.save(commit=False)
        goal.user = self.request.user


        new_category_name = form.cleaned_data.get('new_category')
        selected_category = form.cleaned_data.get('category')


        if new_category_name:
            category, created = Category.objects.get_or_create(
                name=new_category_name,
                defaults={
                    'is_system': False,
                    'created_by': self.request.user
                }
            )
            goal.category = category
        else:
            goal.category = selected_category

        goal.save()
        return super().form_valid(form)