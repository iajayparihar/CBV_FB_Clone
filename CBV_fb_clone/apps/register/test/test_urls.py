import pytest
from django.urls import reverse, resolve
from register.views import *
from django.urls.exceptions import Resolver404

@pytest.mark.parametrize('url_name, expected_view', [
    ('register', register),
    ('profile', profile),
])
def test_urls(url_name, expected_view):
    try:
        url = reverse(f'Register:{url_name}')
        found = resolve(url)
        assert found.func.view_class == expected_view
    except Resolver404:
        pytest.fail(f"Failed to resolve URL: {url}")
