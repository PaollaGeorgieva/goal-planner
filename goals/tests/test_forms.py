from django.test import TestCase
from goals.models import Category, TargetGoal, HabitGoal
from goals.forms import TargetGoalCreateForm, HabitGoalCreateForm
from accounts.models import AppUser


class TestTargetGoalCreateForm(TestCase):
    def setUp(self):

        self.user = AppUser.objects.create_user(
            email='test_target@example.com',
            password='pass123'
        )
        self.system_category = Category.objects.create(
            name='System Category',
            is_system=True
        )
        self.user_category = Category.objects.create(
            name='User Category',
            created_by=self.user
        )
        self.base_data = {
            'goal_type': TargetGoal.TYPE_CHOICES[0][0],
            'title': 'Complete Project',
            'description': 'Finalize tasks',
            'start_date': '2025-08-01',
            'end_date': '2025-09-01'
        }

    def make_form(self, extra_data):
        data = {**self.base_data, **extra_data}
        return TargetGoalCreateForm(data=data, user=self.user)


    def test_missing_category_and_new(self):
        form = self.make_form({'category': '', 'new_category': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_both_selected_and_new(self):
        form = self.make_form({'category': self.user_category.pk, 'new_category': 'NewCat'})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        self.assertIn('new_category', form.errors)

    def test_new_conflicts_system(self):
        form = self.make_form({'category': '', 'new_category': self.system_category.name})
        self.assertFalse(form.is_valid())
        self.assertIn('new_category', form.errors)

    def test_new_conflicts_user(self):
        form = self.make_form({'category': '', 'new_category': self.user_category.name})
        self.assertFalse(form.is_valid())
        self.assertIn('new_category', form.errors)


    def test_valid_with_existing_category(self):
        form = self.make_form({'category': self.system_category.pk, 'new_category': ''})
        self.assertTrue(form.is_valid())


class TestHabitGoalCreateForm(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            email='test_habit@example.com',
            password='pass456'
        )
        self.system_category = Category.objects.create(
            name='Habit System',
            is_system=True
        )
        self.user_category = Category.objects.create(
            name='Habit User',
            created_by=self.user
        )
        self.base_valid = {
            'goal_type': HabitGoal.TYPE_CHOICES[1][0],
            'title': 'Daily Run',
            'description': 'Run 5km',
            'start_date': '2025-08-01',
            'target_per_period': 1,
            'period_unit': HabitGoal.PERIOD_CHOICES[0][0]
        }

    def make_form(self, extra_data):
        data = {**self.base_valid, **extra_data}
        return HabitGoalCreateForm(data=data, user=self.user)


    def test_valid_with_existing_category(self):
        form = self.make_form({'category': self.user_category.pk, 'new_category': ''})
        self.assertTrue(form.is_valid())

