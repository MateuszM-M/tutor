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
from django.views.generic.edit import DeleteView, FormView
from django_filters.views import FilterView

from .filters import CourseFilter
from .forms import CourseEnrollForm, CreateUpdateCourseForm, ModuleFormSet
from .models import Content, Course, Module, Subject


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


class CourseListView(FilterView):
    """
    A class to inherit from for all views that use
    course_list template
    """
    model = Course
    template_name = 'learning/course_list.html'
    filterset_class = CourseFilter
    paginate_by = 10


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    A class to represent main dashboard view.
    """
    template_name = 'learning/dashboard.html'


class TeacherDashboard(OwnerMixin, 
                       CourseListView, 
                       LoginRequiredMixin):
    """
    A class to represent teacher dashboard view.
    """

    def get_context_data(self, *args, **kwargs):
        context = super(TeacherDashboard, self).get_context_data(**kwargs)
        context.update({'courses': self.object_list, 'author': self.request.user,
                        'card_width': 8, 'title': 'Your Courses'})
        return context
    

class CourseCreateView(PermissionRequiredMixin, 
                       OwnerCourseEditMixin,
                       CreateView):
    """
    A class to represent create course view.
    """
    template_name = 'learning/teacher/create_update_course.html'
    success_url = reverse_lazy('learning:teacher_dashboard')
    permission_required = 'learning.add_course'

    def form_valid(self, form):
        """
        Overides form_valid to addtionally assign
        slug from slugyfying the course title
        """
        form.instance.slug = slugify(form.instance.title)
        return super(CourseCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Overrides function to add additional context data
        """
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context.update({'submit_value': 'Create', 'title': 'Create Course'})
        return context
    

class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin, 
                       DeleteView):
    """
    A class to represent delete couse view.
    """
    success_url = reverse_lazy('learning:teacher_dashboard')
    template_name = 'learning/teacher/delete_course.html'
    permission_required = 'learning.delete_course'
    extra_context = {'title': 'Delete'}


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    """
    A class to represent update couse view.
    """
    template_name = 'learning/teacher/create_update_course.html'
    success_url = reverse_lazy('learning:teacher_dashboard')
    permission_required = 'learning.change_course'
    extra_context = {'submit_value': 'Update', 'title': 'Update Course'}


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
        context.update({'enroll_form': CourseEnrollForm(
            initial={'course': self.object}),
            'title': self.object.title,
            'card_width': 8
            })

        return context


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    A class to represent course module update view
    """
    template_name = 'learning/teacher/modules_formset.html'
    course = None

    def get_formset(self, data=None):
        """
        Gets module formset
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
        course = self.course
        formset = self.get_formset()
        return self.render_to_response({'course': course,
                                        'formset': formset,
                                        'title': course.title,
                                        "card_width": 6})
        
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
        obj = self.obj
        if obj:
            title = f"Editing {obj.title}"
        else:
            title = "Adding new content"
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': obj,
                                        'title': title,
                                        'course': self.module.course,
                                        'card_width': 6})

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
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('learning:module_content_list', self.module.id)
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
        return redirect('learning:module_content_list', module.id)
    

class ModuleContentListView(TemplateResponseMixin, View):
    """
    A class to handle the list of content.
    """
    template_name = 'learning/teacher/contents.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        context = {'module': module,
                   'course': module.course,
                   "title": module.title,
                   "course": module.course}
        return self.render_to_response(context)
    

class SubjectListView(CourseListView):
    """
    A class to represent course list filtered by subject 
    """

    def get_queryset(self, slug=None, **kwargs):
        """
        Returns queryset of courses filtered by subject
        """
        qs = super(SubjectListView, self).get_queryset()
        subject = get_object_or_404(Subject, 
                                    slug=self.kwargs['slug'])
        return qs.filter(subject=subject)
    
    def get_context_data(self, **kwargs):
        """
        Updates context
        """
        context = super(SubjectListView, self).get_context_data(**kwargs)
        obj_list = self.get_object_list
        context.update({'courses': obj_list,
                        'title': obj_list[0].subject,
                        'card_width': 8})
        return context


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    A class to represent course enrollment  
    """
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """
        Overrider form_valid to add request user to enrolled students
        """
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                     self).form_valid(form)
        
    def get_success_url(self):
        """
        Redirects user to course detail after successful enrollment.
        """
        return reverse_lazy('learning:detail_course',
                            args=[self.course.slug])
    

class StudentDashboard(LoginRequiredMixin, CourseListView):
    """
    A class to reprsent course list student enrolled to.
    """

    def get_queryset(self):
        """
        Returns queryset of courses student enrolled to.
        """
        qs = super(StudentDashboard, self).get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        """
        Updates context.
        """
        context = super(StudentDashboard, self).get_context_data(**kwargs)
        context.update({'courses': self.object_list, 'title': "Courses",
                        "card_width": 8})
        return context
    

class StudentCourseDetailView(DetailView):
    """
    A class to display contents of module
    """
    model = Course
    template_name = 'learning/student/course_detail.html'
    
    def get_queryset(self):
        """
        Checks if request user is enrolled to the course.
        """
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        """
        Updates context

        if module_id is provided, adds it to context,
        otherwise adds id of first course module
        """

        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)

        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]

        module = context['module']
        context.update({'title': module.title,
                        'card_width': 8})
        return context