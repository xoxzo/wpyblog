
from .views import (
    list_post,
    category_list_post,
    tag_list_post,
    view_post,
    preview_post,
    clear_cache,
)

from django.urls import path

app_name = "wpyblog"

urlpatterns = [
    path("", list_post, name="blog"),
    path("category/<int:category_id>/<slug:slug>/", category_list_post, name="category-post-list"),
    path("tag/<int:tag_id>/<slug:slug>/", tag_list_post, name="tag-post-list"),
    path("<int:post_id>/<slug:slug>/", view_post, name="view-post"),
    path("preview/<int:post_id>/", preview_post, name="preview-post"),
    path("clear/", clear_cache, name="clear-post"),
]
