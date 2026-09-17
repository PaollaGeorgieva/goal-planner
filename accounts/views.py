
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect

from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import  reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import AppUserCreationForm, ProfileEditForm
from accounts.models import Profile

from goals.utils import get_user_statistics, build_activity_calendar

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

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update(get_user_statistics(user))
        context.update(build_activity_calendar(user))
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.pk})

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profile-details', kwargs={'pk': pk})



