from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView


from goals.mixins import GoalListMixin
from goals.simple_goals import GOALS


class LandingPageView(TemplateView):
    template_name = 'common/landing-page.html'


class HomePageView(LoginRequiredMixin,GoalListMixin, TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_goals'] = self.get_recent_goals(limit=4)
        today = timezone.localdate()
        day_number = today.toordinal()

        index = day_number % len(GOALS)


        context['daily_goal'] = GOALS[index]
        context['today'] = today
        return context


