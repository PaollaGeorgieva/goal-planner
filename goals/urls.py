from django.urls import path, include

from goals.views.all_goals_view import AllGoalsView
from goals.views.goal_create_view import GoalCreateView
from goals.views.habit_goal_complete_view import HabitGoalCompleteView
from goals.views.habit_goal_delete_view import HabitGoalDeleteView
from goals.views.habit_goal_update_view import HabitGoalUpdateView
from goals.views.target_goal_complete_view import TargetGoalCompleteView
from goals.views.target_goal_delete_view import TargetGoalDeleteView
from goals.views.target_goal_detail_view import TargetGoalDetailView
from goals.views.target_goal_update_view import TargetGoalUpdateView
from goals.views.habit_goal_details_view import HabitGoalDetailView




urlpatterns = [
    path('create/', GoalCreateView.as_view(), name='create-goal'),
    path('', AllGoalsView.as_view(), name='goals'),
    path('target/<int:pk>/', include([
        path('', TargetGoalDetailView.as_view(), name='target-goal-details' ),
        path('steps/', include(('steps.urls', 'steps'), namespace='steps')),
        path('edit/', TargetGoalUpdateView.as_view(), name='target-goal-edit'),
        path('delete/', TargetGoalDeleteView.as_view(), name='target-goal-delete'),
        path('complete/', TargetGoalCompleteView.as_view(), name='complete-target-goal'),
    ])),

    path('habit/<int:pk>/', include([
       path('', HabitGoalDetailView.as_view(), name='habit-goal-details'),
       path('edit/', HabitGoalUpdateView.as_view(), name='habit-goal-edit'),
        path('delete/', HabitGoalDeleteView.as_view(), name='habit-goal-delete'),
       path('complete/', HabitGoalCompleteView.as_view(), name='complete-habit-goal'),
    ])),



    path('<str:goal_type>/<int:pk>/notes/', include(('notes.urls', 'notes'), namespace='notes')),


]

