from rest_framework.views import APIView
from django.forms.models import model_to_dict
# Create your views here.

from dclass.models import models_dict, models_fields
from rest_framework.response import Response


class ModelList(APIView):
    def get(self, request, fomat=None):
        keys = []
        for key, value in models_dict.iteritems():
            keys.append(key)
        return Response(keys)


class Model(APIView):
    def get(self, request, fomat=None, model=None):
        data = []
        if model:
            chosed_model = models_dict[model]
            data.append(models_fields[model])
            data.append(chosed_model.objects.all().values())
        return Response(data)



class ModelDetails(APIView):
    def get(self, request, pk, fomat=None, model=None):
        data = []
        if model:
            chosed_model = models_dict[model]
            data.append(models_fields[model])
            data.append(model_to_dict(chosed_model.objects.get(pk=pk)))
        return Response(data)

    def post(self, request, pk, fomat=None, model=None):
        data = []
        if model:
            chosed_model = models_dict[model]
            update_data = {request.DATA.get('field'): request.DATA.get('value')}
            chosed_model.objects.filter(pk=pk).update(**update_data)
            data.append(models_fields[model])
            data.append(chosed_model.objects.all().values())
        return Response(data)

