from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class GroupRequiredMixin(LoginRequiredMixin, 
                           UserPassesTestMixin):
    group_required = None

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name=self.group_required).exists()

