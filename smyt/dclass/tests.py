# coding=utf-8
import random
import string
from datetime import date
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from dclass.models import models_dict, models_fields


class ModelsTestCase(TestCase):
    inserted = {}
    def setUp(self):
        record = {}
        #insert values
        for key, value in models_fields.iteritems():
            record = {}
            for field, type in value.iteritems():
                if type.get('type') == 'int':
                    record[field] = random.randrange(100000)
                if type.get('type') == 'chr':
                    record[field] = u''.join([random.choice(string.letters) for i in xrange(20)])
                if type.get('type') == 'date':
                    record[field] = date(random.randrange(1950, 2020), random.randrange(1, 12), random.randrange(1, 28))
            rec = models_dict[key](**record)
            rec.save()
            record['pk'] = rec.pk
            self.inserted[key] = record

    def test_records_is_inserted(self):
        for key, value in self.inserted.iteritems():
            dj_object = models_dict[key].objects.get(pk=value.get('pk'))
            for field in models_fields[key].iterkeys():
                self.assertEqual(value[field], getattr(dj_object, field))


class RestApiTests(APITestCase):

    def test_model_list_class(self):
        """
        тестируем ModelList
        """
        response = self.client.get('/api/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        list = [key for key in models_dict.iterkeys()]
        self.assertListEqual(list, response.data)

    def test_model_class(self):
        """
        тестируем Model
        """
        for key, value in models_fields.iteritems():
            record = {}
            for field, type in value.iteritems():
                if type.get('type') == 'int':
                    record[field] = random.randrange(100000)
                if type.get('type') == 'chr':
                    record[field] = u''.join([random.choice(string.letters) for i in xrange(20)])
                if type.get('type') == 'date':
                    record[field] = date(random.randrange(1950, 2020), random.randrange(1, 12), random.randrange(1, 28))

            response = self.client.post('/api/%s/' % key, record, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in models_fields.iteritems():
            response = self.client.get('/api/%s/' % key, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response.data[0], value)

            for record in response.data[1]:
                dj_object = models_dict[key].objects.get(pk=record.get('id'))
                for field in record.iterkeys():
                    self.assertEqual(record[field], getattr(dj_object, field))

    def test_model_details_class(self):
        """
        тестируем ModelDetails
        """
        inserted = {}
        for key, value in models_fields.iteritems():
            record = {}
            for field, type in value.iteritems():
                if type.get('type') == 'int':
                    record[field] = random.randrange(100000)
                if type.get('type') == 'chr':
                    record[field] = u''.join([random.choice(string.letters) for i in xrange(20)])
                if type.get('type') == 'date':
                    record[field] = date(random.randrange(1950, 2020), random.randrange(1, 12), random.randrange(1, 28))

            response = self.client.post('/api/%s/' % key, record, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            for record in response.data[1]:
                dj_object = models_dict[key].objects.get(pk=record.get('id'))
                rest_object = self.client.get('/api/%s/%s/' % (key, record.get('id')), record, format='json')
                self.assertEqual(rest_object.status_code, status.HTTP_200_OK)
                rest_rec = rest_object.data[1]

                for field in rest_rec.iterkeys():
                    self.assertEqual(rest_rec[field], getattr(dj_object, field))

                for field, type in response.data[0].iteritems():
                    if type.get('type') == 'int':
                        data = dict(field=field,
                                    value=random.randrange(100000))
                    if type.get('type') == 'chr':
                        data = dict(field=field,
                                    value=u''.join([random.choice(string.letters) for i in xrange(20)]))
                    if type.get('type') == 'date':
                        data = dict(field=field,
                                    value=date(random.randrange(1000, 2020), random.randrange(1, 12), random.randrange(1, 28)))

                    if field != 'id':
                        rest_object = self.client.post('/api/%s/%s/' % (key, record.get('id')), data, format='json')

                    self.assertEqual(rest_object.status_code, status.HTTP_200_OK)

                    rest_rec = rest_object.data[1][0]
                    dj_object = models_dict[key].objects.get(pk=record.get('id'))

                    for field in rest_rec.iterkeys():
                        self.assertEqual(rest_rec[field], getattr(dj_object, field))
