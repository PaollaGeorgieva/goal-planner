from collections import OrderedDict
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import AppUserCreationForm, ProfileEditForm
from accounts.models import Profile
from goals.models import TargetGoal, HabitGoal
from goals.utils import calculate_current_streak, get_recent_activity


UserModel = get_user_model()


class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/registration.html'



    def form_valid(self, form):
        self.object = form.save()

        user = authenticate(
            request=self.request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )

        if user is not None:
            login(self.request, user)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('edit-profile', kwargs={'pk': self.object.profile.pk})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user


        goals_created   = (
            TargetGoal.objects.filter(user=user).count() +
            HabitGoal.objects.filter(user=user).count()
        )
        completed_goals = TargetGoal.objects.filter(
            user=user, is_completed=True
        ).count()
        active_habits  = HabitGoal.objects.filter(
            user=user, is_completed=False
        ).count()
        current_streak = calculate_current_streak(user)


        recent_activity = get_recent_activity(user, limit=8)
        recent = get_recent_activity(user, limit=1)
        last_activity = recent[0] if recent else None



        all_activity = get_recent_activity(user, limit=None)


        today       = timezone.localdate()
        start_month = today.replace(day=1)
        month_activity = [
            act for act in all_activity
            if act['activity_date'].date() >= start_month
        ]


        calendar_map = OrderedDict()
        for act in month_activity:
            iso = act['activity_date'].date().isoformat()
            status = 'completed' if act['verb'] == 'Completed' else 'checked-in'
            calendar_map.setdefault(iso, []).append(status)


        context.update({
            'goals_created':   goals_created,
            'completed_goals': completed_goals,
            'active_habits':   active_habits,
            'current_streak':  current_streak,
            'recent_activity': recent_activity,
            'last_activity': last_activity,
            'calendar_map':    dict(calendar_map),
        })
        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'


    def get_object(self, queryset=None):

        return self.request.user.profile

    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user

    def handle_no_permission(self):

        return HttpResponseForbidden("You do not have permission to edit this profile.")


    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.pk})

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profile-details', kwargs={'pk': pk})

def app_user_delete_view(request, pk: int):
    pass


