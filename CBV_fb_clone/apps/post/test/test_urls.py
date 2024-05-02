import pytest
from django.urls import reverse, resolve
from post.views import *
from django.urls.exceptions import Resolver404

@pytest.mark.parametrize('url_name, expected_view, args', [
    ('post', PostFormView, None),
    ('all_user_post', all_user_post, None),
    ('view_post', view_post, None),
    ('update_post', update_post, {'pk': 1}),
    ('delete_post', delete_post, {'pk': 1}),
    ('post_detail', post_detail, {'pk': 1}),
    ('comment_on_post', comment_on_post, {'pk': 1}),
    ('update_on_comment', update_on_comment, None),
    ('delete_comment', delete_comment, None),
    ('like', like, {'pk': 1}),
])
def test_urls(url_name, expected_view, args):
    try:
        url = reverse(f'Post:{url_name}', kwargs=args) if args else reverse(f'Post:{url_name}')
        found = resolve(url)
        assert found.func.view_class == expected_view
        
    except Resolver404:
        pytest.fail(f"Failed to resolve URL: {url}")
