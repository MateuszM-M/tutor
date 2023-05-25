from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class TeacherRequiredMixin(LoginRequiredMixin, 
                           UserPassesTestMixin):
    
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="Teachers").exists()

