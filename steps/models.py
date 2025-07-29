# models.py
from django.db import models
from goals.models import TargetGoal  # adjust import path as needed

class Step(models.Model):
    target_goal = models.ForeignKey(
        TargetGoal,
        related_name='steps',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.completed and self.completed_at is None:
            from django.utils import timezone
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)







    def __str__(self):
        status = '✓' if self.completed else '✗'
        return f"{status} {self.title}"

