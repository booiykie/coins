"""Test module."""
import time
from unittest import mock
from unittest import TestCase
from datetime import datetime, timedelta
from django.test import override_settings
from django.test import Client, RequestFactory

from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.decorators import api_view

from .helpers import datetime_conversion, string_date_to_datetime_format, \
    extract_coin_request_params, offset_resolver, cache_key_generator, DATE_FORMART


class DateParserTest(TestCase):
    date_string = '2020/08/05'
    date_time_string = '2020-08-05 00:00:00'
    incorrect_date_str = '20-08-06'
    
    def test_date_string(self):
        date_object = string_date_to_datetime_format(self.date_string)
        self.assertEqual(str(date_object), self.date_time_string)

    def test_offset(self):
        # how can I test variable days in months and year.
        self.assertEqual(offset_resolver('h', 0), timedelta(hours=0))
        self.assertEqual(offset_resolver('h', 1), timedelta(seconds=3600))
        self.assertEqual(offset_resolver('h', 2), timedelta(seconds=7200))
        self.assertEqual(offset_resolver('m', 1), timedelta(seconds=60))
        self.assertEqual(offset_resolver('M', 1), timedelta(days=30))
        self.assertEqual(offset_resolver('Y', 1), timedelta(days=365))

    def test_invalid_offset(self):
        try:
            self.assertNotEqual(offset_resolver('H', 1), timedelta(seconds=3600))
        except Exception as e:
            self.assertEqual(e.__str__(), 'invalid time offset. Use h, m, M or Y.')


class ParamsTest(TestCase):
    
    def setUp(self):
        self.api_client = Client()

    def test_params_extract(self):
        response = self.api_client.get(
            '/marketCap/', 
            {'coin_id': 'ripple', 'date': '2020/08/05', 'currency': 'gbp'}, 
            HTTP_ACCEPT='application/json', content_type='json'
        )
        response.render()
        drf_request = response.renderer_context['request']
        params = extract_coin_request_params(drf_request)
        self.assertEqual(
            params, ('ripple', datetime.strptime('2020/08/05', DATE_FORMART), 'gbp')
        )

    def test_pending_params(self):
        try:
            response = self.api_client.get(
                '/marketCap/', 
                {'coin_id': 'ripple', 'currency': 'gbp'}, 
                HTTP_ACCEPT='application/json', content_type='json'
            )
            response.render()
            drf_request = response.renderer_context['request']
            params = extract_coin_request_params(drf_request)
        except Exception as e:
            self.assertEqual(e.__str__(), "Missing param: ['date']")

    def test_no_params(self):
        try:
            response = self.api_client.get(
                '/marketCap/', 
                {'coin_id': 'ripple'}, 
                HTTP_ACCEPT='application/json', content_type='json'
            )
            response.render()
            drf_request = response.renderer_context['request']
            params = extract_coin_request_params(drf_request)
        except Exception as e:
            self.assertEqual(e.__str__(), "Missing param: ['currency', 'date']")


    def test_cache_key_genrator(self):
        key = cache_key_generator(
            'ripple', datetime.strptime('2020/08/05', DATE_FORMART), 'gbp')
        self.assertEqual(key, 'ripple_2020-08-05 00-00-00_gbp_1')
        

class ThrottleApiTest(APITestCase):
    TESTING_THRESHOLD = 5
    
    @override_settings(THROTTLE_THRESHOLD=TESTING_THRESHOLD)
    def test_check_coinlist(self):
        client = APIClient()
        _url = '/coinList/'
        for i in range(0, self.TESTING_THRESHOLD):
            client.get(_url)

        # this call should err
        response = client.get(_url)
        # 429 - too many requests
        self.assertEqual(response.status_code, 429)
