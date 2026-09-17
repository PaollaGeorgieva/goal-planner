from datetime import datetime, time, timedelta

from django.utils import timezone

from goals.models import TargetGoal, HabitGoal, HabitCheck
from steps.models import Step

def calculate_current_streak(user) -> int:

    current_date = timezone.localdate()
    streak = 0


    habits = HabitGoal.objects.filter(user=user, is_completed=False)


    checked_dates = set(
        HabitCheck.objects
            .filter(habit__in=habits)
            .values_list('date', flat=True)
    )


    while current_date in checked_dates:
        streak += 1
        current_date -= timedelta(days=1)

    return streak




def build_activity(verb, name, activity_date):

    if not isinstance(activity_date, datetime):
        activity_date = datetime.combine(activity_date, time.min)

    if timezone.is_naive(activity_date):
        activity_date = timezone.make_aware(
            activity_date,
            timezone.get_current_timezone(),
        )

    return {
        "verb": verb,
        "name": name,
        "activity_date": activity_date,
    }


def get_recent_activity(user, limit=5):

    activities = []

    target_goals = TargetGoal.objects.filter(
        user=user,
        is_completed=True,
        completed_at__isnull=False,
    ).values_list("title", "completed_at")

    for title, completed_at in target_goals:
        activities.append(build_activity("Completed", title, completed_at))

    habit_goals = HabitGoal.objects.filter(
        user=user,
        is_completed=True,
        completed_at__isnull=False,
    ).values_list("title", "completed_at")

    for title, completed_at in habit_goals:
        activities.append(build_activity("Completed", title, completed_at))

    completed_steps = Step.objects.filter(
        target_goal__user=user,
        completed=True,
        completed_at__isnull=False,
    ).values_list("title", "completed_at")

    for title, completed_at in completed_steps:
        activities.append(build_activity("Completed step", title, completed_at))

    habit_checks = HabitCheck.objects.filter(habit__user=user,).values_list("habit__title", "date")

    for title, check_date in habit_checks:
        activities.append(build_activity("Checked in", title, check_date))


    activities.sort(
        key=lambda activity: activity["activity_date"],
        reverse=True,
    )

    if limit is None:
        return activities

    return activities[:limit]



def get_user_statistics(user):

    goals_created = (
            TargetGoal.objects.filter(user=user).count() +
            HabitGoal.objects.filter(user=user).count()
    )
    completed_goals = TargetGoal.objects.filter(user=user, is_completed=True).count()
    active_habits = HabitGoal.objects.filter(user=user, is_completed=False).count()
    current_streak = calculate_current_streak(user)

    return {
        "goals_created": goals_created,
        "completed_goals": completed_goals,
        "active_habits": active_habits,
        "current_streak": current_streak,
    }


def build_activity_calendar(user):
    all_activities = get_recent_activity(user, limit=None)
    recent_activities = all_activities[:8]
    last_activity = all_activities[0] if all_activities else None

    today = timezone.localdate()
    start_month = today.replace(day=1)
    monthly_activities = [
        activity for activity in all_activities
        if timezone.localdate(activity['activity_date']) >= start_month
    ]

    calendar_map = {}
    for activity in monthly_activities:
        date_key = timezone.localdate(activity['activity_date']).isoformat()
        if activity['verb'] in ('Completed', 'Completed step'):
            status = 'completed'
        else:
            status = 'checked-in'
        calendar_map.setdefault(date_key, []).append(status)

    return {
        'recent_activity': recent_activities,
        'last_activity': last_activity,
        'calendar_map': calendar_map,
    }
