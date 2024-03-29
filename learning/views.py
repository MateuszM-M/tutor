from django.apps import apps
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from users.models import Profile

from .filters import CourseFilter
from .forms import CreateUpdateCourseForm, ModuleFormSet
from .models import Content, Course, Module


class OwnerMixin(object):
    """
    A mixin that overrides the queryset to filter objects by request user
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin(object):
    """
    A mixin for creation and update, 
    which assings course owner to request user
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    """
    A mixin that assing model to course
    """
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    A mixin that assings form and succes_url
    """
    form_class = CreateUpdateCourseForm
    success_url = reverse_lazy('learning:teacher_dashboard')


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    A class to represent main dashboard view.
    """
    template_name = 'learning/dashboard.html'


class TeacherDashboard(OwnerCourseMixin, FilterView):
    """
    A class to represent teacher dashboard view.
    """
    template_name = 'learning/teacher/teacher_dashboard.html'
    paginate_by = 10
    filterset_class = CourseFilter
        

class CourseCreateView(PermissionRequiredMixin, 
                       OwnerCourseEditMixin,
                       CreateView):
    """
    A class to represent create course view.
    """
    template_name = 'learning/teacher/create_course.html'
    success_url = reverse_lazy('learning:teacher_dashboard')
    permission_required = 'learning.add_course'

    def form_valid(self, form):
        """
        Overides the form validation to addtionally assign
        slug from slugyfying the course title
        """
        form.instance.slug = slugify(form.instance.title)
        return super(CourseCreateView, self).form_valid(form)
    

class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin, 
                       DeleteView):
    """
    A class to represent delete couse view.
    """
    success_url = reverse_lazy('learning:teacher_dashboard')
    template_name = 'learning/teacher/delete_course.html'
    permission_required = 'learning.delete_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    """
    A class to represent update couse view.
    """
    template_name = 'learning/teacher/update_course.html'
    success_url = reverse_lazy('learning:teacher_dashboard')
    permission_required = 'learning.change_course'


class CourseDetailView(OwnerCourseMixin, DetailView):
    """
    A class to represent detail course view for user that
    is interested in buying a course.
    """
    template_name = 'learning/student/course_overview.html'

    def get_context_data(self, **kwargs):
        """
        Adds profile to context to make it accessible from templates.
        """
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(
            id=self.object.owner.profile.id)
        return context


class LearningView(DetailView, LoginRequiredMixin):
    """
    A class to represent learning view for user that bought course.
    """
    model = Course
    template_name = 'learning/student/learning_view.html'

    def get_context_data(self, *args, **kwargs):
        """
        Adds self.object as course to the context so it can be retrieved
        in other templates such as CourseModelUpdateView.
        """
        context = super(LearningView, self).get_context_data(*args, **kwargs)
        context['course'] = self.object
        return context


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    A class to represent course module update view
    """
    template_name = 'learning/teacher/modules_formset.html'
    course = None

    def get_formset(self, data=None):
        """
        Creates module formset
        """
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """
        Handles course to use in get and update methods.
        """
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """
        Renders course and formset on get request.
        """
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
        
    def post(self, request, *args, **kwargs):
        """
        Handles formset and course on post request.
        """
        course = self.course
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('learning:learning_view', slug=course.slug)
        return self.render_to_response({'course': course,
                                        'formset': formset})
    

class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    A class to represent content creation and update view.
    """
    module = None
    model = None
    obj = None
    template_name = 'learning/teacher/create_update_content.html'

    def get_model(self, model_name):
        """
        Checks if model name is one content types.
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='learning',
                                  model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        """
        Dynamically builds form.
        """
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        """
        Handles class parameters.
        """
        self.module = get_object_or_404(Module,
                                       id=module_id,
                                       course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,
           self).dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        """
        Handels get method.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj,
                                        'course': self.module.course})

    def post(self, request, module_id, model_name, id=None):
        """
        Handles post method.
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})
    

class ContentDeleteView(View):
    """
    A class to handle deleting a content.
    """
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)
    

class ModuleContentListView(TemplateResponseMixin, View):
    """
    A class to handle the list of content.
    """
    template_name = 'learning/teacher/contents.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module,
                                        'course': module.course})