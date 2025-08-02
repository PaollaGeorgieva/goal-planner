import datetime

from django.db import models
from django.contrib.auth import get_user_model

from django.utils import timezone
User = get_user_model()



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'accounts.AppUser',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_system', 'name']

    def __str__(self):
        return self.name

class Goal(models.Model):
    TYPE_CHOICES = [
        ('target', 'Target Goal'),
        ('habit', 'Habit'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TargetGoal(Goal):
    end_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)


    def progress_percent(self):
        total_steps = self.steps.count()
        if total_steps == 0:
            return 0
        completed_steps = self.steps.filter(completed=True).count()
        return int((completed_steps / total_steps) * 100)

    def can_be_completed(self):
        qs = self.steps.all()
        return (not qs.exists()) or all(s.completed for s in qs)

    def mark_as_completed(self):

        if not self.can_be_completed():
            raise ValueError("All steps must be completed first.")
        self.is_completed = True

        if self.completed_at is None:
            self.completed_at = timezone.now()
        super().save(update_fields=['is_completed','completed_at'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class HabitGoal(Goal):
    PERIOD_CHOICES = [
        ('day', 'Day'),
        ('week', 'Week'),
    ]
    target_per_period = models.PositiveIntegerField(default=1)
    period_unit = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    completed_at = models.DateTimeField(null=True, blank=True)


    def get_current_period_checks(self, today=None):

        if today is None:
            today = datetime.date.today()

        if self.period_unit == 'week':

            start = today - datetime.timedelta(days=today.weekday())
            end = start + datetime.timedelta(days=7)
        else:  # 'day'
            start = today
            end = today + datetime.timedelta(days=1)

        return self.checks.filter(date__gte=start, date__lt=end).count()

    def progress_percent(self):

        checks = self.get_current_period_checks()
        if self.target_per_period == 0:
            return 0
        return min(100, int((checks / self.target_per_period) * 100))

    def mark_as_completed(self):

        self.is_completed = True
        if self.completed_at is None:
            self.completed_at = timezone.now()
        super().save(update_fields=['is_completed', 'completed_at'])

    def save(self, *args, **kwargs):

        if self.pk is not None:
            old = HabitGoal.objects.get(pk=self.pk)
            if old.is_completed:
                raise ValueError("Cannot modify a completed habit goal.")
        super().save(*args, **kwargs)


class HabitCheck(models.Model):
    habit = models.ForeignKey(HabitGoal, related_name='checks', on_delete=models.CASCADE)
    date = models.DateField()



