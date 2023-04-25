from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    """
    A class to represent custom OrderField. 
    It sets order of the objects and sets object as last if 
    value is not provided.
    """
    
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)
        
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.for_fields.objects.all()
                if self.for_fields:
                    query = {fields: getattr(model_instance, field) for field in self.for_field}
                    qs = qs.filter(**query)
                last_item = qs.filter(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField,
                        self).pre_save(model_instance, add)