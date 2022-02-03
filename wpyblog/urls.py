
from .views import (
    list_post,
    category_list_post,
    tag_list_post,
    view_post,
    preview_post,
    clear_cache,
)

# Django > 3
try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

app_name = "wpyblog"

urlpatterns = [
    url(r"category/(?P<category_id>\d+)/(?P<slug>[-\w]+)/", category_list_post, name="category-post-list"),
    url(r"^tag/(?P<tag_id>\d+)/(?P<slug>[-\w]+)/", tag_list_post, name="tag-post-list"),
    url(r"^(?P<post_id>\d+)/(?P<slug>[-\w]+)/", view_post, name="view-post"),
    url(r"^preview/(?P<post_id>\d+)/", preview_post, name="preview-post"),
    url("^clear/", clear_cache, name="clear-post"),
    url("", list_post, name="blog"),
]
