from django.test import TestCase
from goals.models import  TargetGoal, HabitGoal
import datetime
from accounts.models import AppUser



class TestTargetGoalModelMethods(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(email='model_target@example.com', password='pass')
        self.target = TargetGoal.objects.create(
            user=self.user,
            goal_type='target',
            title='Target',
            description='Description',
            start_date='2025-01-01',
            end_date='2025-12-31'
        )

        for completed in [True, False, True]:
            self.target.steps.create(title='Step', completed=completed)

    def test_progress_percent(self):
        percent = self.target.progress_percent()
        self.assertEqual(percent, 66)

    def test_progress_zero_steps(self):
        new_goal = TargetGoal.objects.create(
            user=self.user,
            goal_type='target',
            title='No Steps',
            description='',
            start_date='2025-01-01',
            end_date='2025-12-31'
        )
        self.assertEqual(new_goal.progress_percent(), 0)

    def test_can_be_completed(self):
        self.assertFalse(self.target.can_be_completed())
        self.target.steps.update(completed=True)
        self.assertTrue(self.target.can_be_completed())

    def test_mark_as_completed_errors(self):
        with self.assertRaises(ValueError):
            self.target.mark_as_completed()

    def test_mark_as_completed_success(self):
        self.target.steps.update(completed=True)
        self.target.mark_as_completed()
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_completed)
        self.assertIsNotNone(self.target.completed_at)


class TestHabitGoalModelMethods(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(email='model_habit@example.com', password='pass')
        self.habit = HabitGoal.objects.create(
            user=self.user,
            goal_type='habit',
            title='Habit',
            description='Description',
            start_date='2025-01-01',
            target_per_period=5,
            period_unit='day'
        )
        today = datetime.date.today()
        for _ in range(3):
            self.habit.checks.create(date=today)

    def test_get_current_period_checks_day(self):
        count = self.habit.get_current_period_checks()
        self.assertEqual(count, 3)

    def test_progress_percent_habit(self):
        self.assertEqual(self.habit.progress_percent(), 60)



