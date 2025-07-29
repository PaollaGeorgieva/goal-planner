from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().user.pk