import random
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


from goals.mixins import GoalListMixin
from goals.models import SimpleGoal


class LandingPageView(TemplateView):
    template_name = 'common/landing-page.html'


class HomePageView(LoginRequiredMixin,GoalListMixin, TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_goals'] = self.get_recent_goals(limit=4)
        simple_goals = list(SimpleGoal.objects.all())
        if simple_goals:
            today_str = date.today().strftime("%Y%m%d")
            day_number = int(today_str)

            index = day_number % len(simple_goals)

            context['daily_goal'] = simple_goals[index].title
        else:
            context['daily_goal'] = "No goals available"
        return context


