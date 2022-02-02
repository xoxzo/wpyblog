# WPYBLOG

## Features

- Enable blog feature for Django application via WordPress Rest API
- Browse by post list
- View single post
- Browse by category
- Browse by tag
- Caching for post list and single post
- Draft post preview (need authentication)

## WordPress Setup

- Enable pretty permalink `yourdomain.com/wp-admin/options-permalink.php`
- Install WP Rest Cache https://wordpress.org/plugins/wp-rest-cache/

## WordPress Multi Language

- Install Polylang plugin
- Install https://github.com/lalokalabs/wp-rest-polylang/

## Draft post preview

1) Set the API credentials in your .env

```
BLOG_USER=apiuser
BLOG_PASS=apiuserpass
```

2) Preview the draft post

` yourdomain.com/blog/preview/<post_id>/`

## Manually clearing post cache

Visit ` yourdomain.com/blog/clear/` to manually clear cache

## Django templates example

post_list.html

```
{% for post in posts %}
    
      <a href="{% url 'wpyblog:view-post' post_id=post.id slug=post.slug %}">
        
          <!-- post thumbnail -->
          <div class="mb-5">
            {% if post.jetpack_featured_media_url and post.jetpack_featured_media_url.strip %}
            <img src="{{ post.jetpack_featured_media_url }}" alt="{{ post.title.rendered|safe }}" class="object-cover">
            {% else %}
            <img src="{% static 'getotp-thumbnail.png' %}" alt="{{ post.title.rendered|safe }}" class="object-cover">
            {% endif %}
          </div>
          <!-- end post thumbnail -->
          <p class="">{{ post.date|string_to_date }}</p>
          <h2 class="">
            {{ post.title.rendered|safe }}
          </h2>
          <!-- post excerpt -->
          <div class="">
            {{ post.excerpt.rendered|safe }}
          </div>
          <!-- end post excerpt -->
        </article>
      </a>
    </div>
    {% endfor %}
```

view_post.html

```
    <a href="{% url 'wpyblog:view-post' post_id=post.id slug=post.slug %}"><h2 class="">{{ post.title.rendered|safe }}</h2></a>
    <p class="">
        {{ post.date|string_to_date }}
        <span class="">·</span>
        {{ author_name }}
    </p>

    <!-- post content -->
    <div class="prose prose-sm md:prose">
        {{ post.content.rendered|safe }}
    </div>
    <!-- end post content -->

    {% if post_tags %}
    <div class="">
        <p class="">{% translate 'Tags' %} :</p>
        {% for post_tag in post_tags %}
        <a href="{% url 'wpyblog:tag-post-list' tag_id=post_tag.id slug=post_tag.slug %}" class="">{{ post_tag.name }}</a>
        {% endfor %}
    </div>
    {% endif %}
```
