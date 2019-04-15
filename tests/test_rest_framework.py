from __future__ import unicode_literals

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from dj_rql.rest_framework import RQLFilterBackend
from tests.dj_rf.models import Book


@pytest.fixture
def api_client():
    client = APIClient()
    client.default_format = 'json'
    return client


@pytest.mark.django_db
def test_list(api_client):
    books = [Book.objects.create() for _ in range(2)]
    response = api_client.get(reverse('book-list') + '?')
    assert response.status_code == HTTP_200_OK
    assert response.data == [{'id': books[0].pk}, {'id': books[1].pk}]


@pytest.mark.django_db
def test_list_empty(api_client):
    response = api_client.get(reverse('book-list'))
    assert response.status_code == HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_list_filtering(api_client):
    books = [Book.objects.create() for _ in range(2)]
    query = 'id={}'.format(books[0].pk)
    response = api_client.get('{}?{}'.format(reverse('book-list'), query))
    assert response.status_code == HTTP_200_OK
    assert response.data == [{'id': books[0].pk}]


def test_rql_filter_cls_is_not_set():
    class View(object):
        pass

    with pytest.raises(AssertionError) as e:
        RQLFilterBackend().filter_queryset(None, None, View())
    assert str(e.value) == 'RQL Filter Class must be set in view.'


def test_rql_filter_cls_wrong_base_cls():
    class Filter(object):
        pass

    class View(object):
        rql_filter_class = Filter

    with pytest.raises(AssertionError) as e:
        RQLFilterBackend().filter_queryset(None, None, View())
    assert str(e.value) == 'Filtering class must subclass RQLFilterClass.'
