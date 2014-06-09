from rest_framework.views import APIView
from django.forms.models import model_to_dict
# Create your views here.

from dclass.models import models_dict
from rest_framework.response import Response


class ModelList(APIView):
    def get(self, request, fomat=None):
        keys = []
        for key, value in models_dict.iteritems():
            keys.append(key)
        return Response(keys)


class Model(APIView):
    def get(self, request, fomat=None, model=None):
        data = None
        if model:
            chosed_model = models_dict[model]
            print type(chosed_model._meta.fields[0].__class__)
            data = chosed_model.objects.all().values()
        return Response(data)


class ModelDetails(APIView):
    def get(self, request, pk, fomat=None, model=None):
        data = None
        if model:
            chosed_model = models_dict[model]
            data = model_to_dict(chosed_model.objects.get(pk=pk))
        return Response(data)


class ModelDetails(APIView):
    def get(self, request, pk, fomat=None, model=None):
        if model:
            chosed_model = models_dict[model]
            data = type(chosed_model._meta.fields[0])
        return Response(data)


