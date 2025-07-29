from django.urls import path, include

from api.views.goal_views import AllGoalsAPIView, TargetGoalCreateSet, TargetGoalViewSet, HabitGoalCreateSet, \
    HabitGoalViewSet
from api.views.notes_views import NoteListCreateView, NoteRUDView
from api.views.steps_views import StepListCreateView, StepRUDView

urlpatterns = [
    path('goals/', AllGoalsAPIView.as_view(), name='api-all-goals'),
    path('target/', include([
             path('', TargetGoalCreateSet.as_view(), name='api-create-goal'),
            path('<int:pk>/', TargetGoalViewSet.as_view(), name='target'),

            path('<int:pk>/steps/',StepListCreateView.as_view(),name='step-list-create'
                ),
                path(
                    '<int:pk>/steps/<int:step_pk>/',
                    StepRUDView.as_view(),
                    name='step-rud'
                ),
                    ])),
    path('habit/', include([
            path('', HabitGoalCreateSet.as_view(), name='api-create-habit'),
            path('<int:pk>/', HabitGoalViewSet.as_view(), name='habit'),
        ])),
    path(
        '<str:goal_type>/<int:pk>/notes/',
        NoteListCreateView.as_view(),
        name='note-list-create'
    ),
    path(
        '<str:goal_type>/<int:pk>/notes/<int:note_pk>/',
        NoteRUDView.as_view(),
        name='note-rud'
    ),


]