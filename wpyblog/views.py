from django.template.response import TemplateResponse
from django.conf import settings
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.utils.encoding import uri_to_iri
from django.utils import translation

import requests
import requests_cache

ONE_HOUR = 60 * 60
HALF_DAY = ONE_HOUR * 12
ONE_DAY = ONE_HOUR * 24
ONE_WEEK = ONE_DAY * 7

timeout = settings.__dict__.get('BLOG_TIMEOUT', 5)

WPYBLOG_REQUESTS_CACHE_ENABLE = settings.__dict__.get('WPYBLOG_REQUESTS_CACHE_ENABLE', True)
cache_key = settings.__dict__.get('WPYBLOG_CACHE', 'wpyblog_cache')

if WPYBLOG_REQUESTS_CACHE_ENABLE:
    requests_cache.install_cache(cache_key)


@cache_page(ONE_DAY)
def list_post(request):
    print("CCCCCCCCCCXXXX")
    return get_post_list(request)

@cache_page(ONE_DAY)
def category_list_post(request, category_id, slug):
    return get_post_list(request = request, category_id = category_id)

@cache_page(ONE_DAY)
def tag_list_post(request, tag_id, slug):
    return get_post_list(request = request, tag_id = tag_id)

@cache_page(ONE_DAY)
def view_post(request, post_id, slug):
    return get_single_post(request, post_id)

# preview draft post
def preview_post(request, post_id):
    return get_single_post(request, post_id)

def get_single_post(request, post_id):
    context = {}

    post = get_post(post_id)
    if post is None:
        raise Http404()

    post = _process_post(post)
    post["slug"] = uri_to_iri(post["slug"])

    author_name = post["_embedded"]["author"][0]["name"]
    post_categories = post["_embedded"]["wp:term"][0]
    post_tags = post["_embedded"]["wp:term"][1]

    context["post"] = post
    context["author_name"] = author_name
    context["post_categories"] = post_categories
    context["post_tags"] = post_tags
    context["categories"] = get_categories(request.LANGUAGE_CODE)

    response = TemplateResponse(request, "wpyblog/view_post.html", context)

    return response

def get_post_list(request, category_id = None, tag_id = None):
    context = {}

    page_number = request.GET.get('page', 1)

    posts_data = get_posts_data(page_number, category_id, tag_id)

    pagination = get_pagination_data(page_number, posts_data["total_pages"], posts_data["count"])

    context["posts"] = posts_data["posts"]
    context["categories"] = get_categories(request.LANGUAGE_CODE)
    context["pagination"] = pagination

    response = TemplateResponse(request, "wpyblog/post_list.html", context)

    return response         

def _process_post(post):
    current_lang = translation.get_language()
    post["slug"] = uri_to_iri(post["slug"])
    if post["polylang_current_lang"] == "en_US":
        post["polylang_current_lang"] = "en"
    for count, post_trans in enumerate(post["polylang_translations"]):
        if post_trans["locale"] == "en_US":
            post["polylang_translations"][count]["locale"] = "en"
        post["polylang_translations"][count]["slug"] = uri_to_iri(post["polylang_translations"][count]["slug"])
    return post

def get_posts_data(page_number, category_id = None, tag_id = None):
    
    posts_data = {}
    
    posts = []

    url = settings.BLOG_URL + "/wp-json/wp/v2/posts"

    if category_id is not None:
        url = url + "?categories=" + str(category_id)

    if tag_id is not None:
        url = url + "?tags=" + str(tag_id)    

    query_params = {
        'page': page_number,
        'per_page': 9
    }

    response = requests.get(url, query_params, timeout=timeout, auth=get_blog_access())
    
    posts = response.json()
    count = response.headers.get("X-WP-Total")
    total_pages = response.headers.get("X-WP-TotalPages")

    current_lang = translation.get_language()
    def filter_lang(post):
        if post["polylang_current_lang"] == current_lang:
            return True
        return False

    posts_data["posts"] = map(_process_post, posts)
    posts_data["posts"] = list(filter(filter_lang, posts_data["posts"]))
    posts_data["count"] = count
    posts_data["total_pages"] = total_pages
    
    return posts_data

def get_pagination_data(page_number, total_pages, count):

    total_pages = int(total_pages)
    count = int(count)

    pagination_data = {}
    
    prev_link = ''
    next_link = ''

    previous_page_number = int(page_number) - 1
    next_page_number = int(page_number) + 1

    has_previous = False
    has_next = False

    if previous_page_number > 0:
        has_previous = True

    if next_page_number <= total_pages:
        has_next = True

    prev_link = reverse('wpyblog:blog') + "?page=" + str(previous_page_number)
    next_link = reverse('wpyblog:blog') + "?page=" + str(next_page_number)

    pagination_data["previous_page_number"] = previous_page_number
    pagination_data["next_page_number"] = next_page_number
    pagination_data["has_previous"] = has_previous
    pagination_data["has_next"] = has_next
    pagination_data["num_pages"] = total_pages
    pagination_data["count"] = count

    # pagination link
    pagination_data["prev_link"] = prev_link
    pagination_data["next_link"] = next_link

    return pagination_data

def get_post(post_id):

    post = {}

    url = settings.BLOG_URL + "/wp-json/wp/v2/posts/" + str(post_id) + "?_embed"

    response = requests.get(url, timeout=timeout, auth=get_blog_access())
    if response.status_code != 200:
        return None
    post = response.json()

    return post

def get_categories(lang="en"):
    categories = []

    url = settings.BLOG_URL + "/wp-json/wp/v2/categories?hide_empty=1&lang=" + lang

    response = requests.get(url)
    categories = response.json()

    def _process_category(category):
        category["slug"] = uri_to_iri(category["slug"])
        return category

    categories = map(_process_category, categories)

    return categories

# return username and password for API Basic Auth
def get_blog_access():
    return (settings.BLOG_USER, settings.BLOG_PASS)

def clear_cache(request):
    cache.clear()
    return HttpResponse('blog cache cleared!')
