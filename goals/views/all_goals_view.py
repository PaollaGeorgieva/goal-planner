from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from goals.forms import SearchForm
from goals.mixins import GoalListMixin



class AllGoalsView(LoginRequiredMixin,GoalListMixin, ListView):
    template_name = 'goals/goals-page.html'
    context_object_name = 'goals'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('query')
        filtered_goals = self.get_filtered_user_goals() # we get the filtered goals based on the category
        if query:
            filtered_goals = [goal for goal in filtered_goals if query.lower() in goal.title.lower()]

        return filtered_goals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_category = self.request.GET.get('category', 'All')
        all_goals = self.get_all_user_goals()


        active_categories = {g.category for g in all_goals if not g.is_completed}
        all_categories = self.get_all_user_categories()
        filtered_categories = [cat for cat in all_categories if cat in active_categories]

        context.update({
            'search_form': SearchForm(initial={'query': self.request.GET.get('query', '')}),
            'selected_category': selected_category,
            'recent_goals': self.get_recent_goals(),
            'categories': filtered_categories,
            'show_completed': any(g.is_completed for g in all_goals),
        })

        return context
