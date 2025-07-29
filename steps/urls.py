from django.urls import path
from steps.views import StepsView, StepCreateView, StepToggleCompleteView, StepEditView, StepDeleteView

app_name = 'steps'

urlpatterns = [
    path('', StepsView.as_view(), name='step-list'),
    path('create/', StepCreateView.as_view(), name='step-create'),
    path('<int:step_id>/toggle/', StepToggleCompleteView.as_view(), name='toggle-step'),
    path('<int:step_id>/edit/', StepEditView.as_view(), name='edit-step'),
    path('<int:step_id>/delete/', StepDeleteView.as_view(), name='delete-step')

]