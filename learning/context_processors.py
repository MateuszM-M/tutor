from .models import Subject


def subjects_processor(request):
    """
    A context processor that allows to  prosses subject
    objects in every template.
    """
    subjects = Subject.objects.all()            
    return {'subjects': subjects}
