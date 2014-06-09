# coding=utf-8
from django.db import models


def gen_model(key, value):
    fields = dict()
    for field in value.get('fields'):

        if field.get('type') == 'int':
            fields[field.get('id')] = models.IntegerField(field.get('title'))
        elif field.get('type') == 'date':
            fields[field.get('id')] = models.DateField(field.get('title'))
        elif field.get('type') == 'chr':
            fields[field.get('id')] = models.CharField(field.get('title'),
                                                       max_length=40)

    fields['__unicode__'] = lambda self: '%s' % self.id

    meta = type('Meta', (), {'verbose_name': value.get('title'),
                             'verbose_name_plural': value.get('title_plural')})

    fields['__module__'] = 'dclass.models'
    fields['Meta'] = meta
    model = type(key, (models.Model,), fields)
    return model
