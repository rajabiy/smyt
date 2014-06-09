# coding=utf-8
import yaml
from django.contrib import admin
from smyt.settings import YAML_FILE
from dclass.cgenerator import gen_model

yaml_models = yaml.load(open(YAML_FILE))

models_dict = dict()
models_fields = dict()

for key, value in yaml_models.iteritems():
    model = gen_model(key, value)
    admin.site.register(model)
    models_dict[model._meta.verbose_name] = model

    fields = {'id': {'title': 'id', 'type': 'int'}}

    for field in value.get('fields'):
        fields[field.get('id')] = field

    models_fields[model._meta.verbose_name] = fields

