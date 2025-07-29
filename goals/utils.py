

from django.db.models import Value, F, CharField
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from goals.models import TargetGoal, HabitGoal, HabitCheck
from steps.models import Step
from typing import List, Dict, Any


def calculate_current_streak(user) -> int:

    today = timezone.localdate()
    streak = 0


    habits = HabitGoal.objects.filter(user=user, is_completed=False)


    checked_dates = set(
        HabitCheck.objects
            .filter(habit__in=habits)
            .values_list('date', flat=True)
    )


    while today in checked_dates:
        streak += 1
        today -= timedelta(days=1)

    return streak


def get_recent_activity(user, limit: int = 5) -> List[Dict[str, Any]]:

    tz = timezone.get_current_timezone()

    def fetch_activities(queryset, verb_label: str, name_field: str, date_field: str):
        return (
            queryset
            .annotate(
                verb=Value(verb_label, output_field=CharField()),
                name=F(name_field),
                raw_date=F(date_field),
            )
            .values('verb', 'name', 'raw_date')
        )

    target_qs = fetch_activities(
        TargetGoal.objects.filter(user=user, is_completed=True, completed_at__isnull=False),
        'Completed', 'title', 'completed_at'
    )


    habit_qs = fetch_activities(
        HabitGoal.objects.filter(user=user, is_completed=True, completed_at__isnull=False),
        'Completed', 'title', 'completed_at'
    )

    check_qs = fetch_activities(
        HabitCheck.objects.filter(habit__user=user),
        'Checked in', 'habit__title', 'date'
    )


    step_qs = fetch_activities(
        Step.objects.filter(target_goal__user=user, completed=True, completed_at__isnull=False),
        'Completed step', 'title', 'completed_at'
    )

    # Merge
    activities: List[Dict[str, Any]] = []
    for record in list(target_qs) + list(habit_qs) + list(step_qs) + list(check_qs):
        raw_date = record.pop('raw_date')
        if isinstance(raw_date, datetime):
            dt = raw_date
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, tz)
        else:
            dt = datetime.combine(raw_date, time.min)
            dt = timezone.make_aware(dt, tz)

        activities.append({**record, 'activity_date': dt})

    activities.sort(key=lambda x: x['activity_date'], reverse=True)
    return activities[:limit] if limit is not None else activities