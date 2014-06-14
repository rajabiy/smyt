# coding=utf-8
from rest_framework import serializers
from dclass.models import models_dict


serializers_dict = dict()

#Генерерируем сериализаторы для моделей
for key, value in models_dict.iteritems():
    meta = type('Meta', (), {'model': value})
    serializer = type('Ser%s' % value.__name__, (serializers.ModelSerializer,), {'Meta': meta})
    serializers_dict[key] = serializer