from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()

@register.filter(name="string_to_date")
def string_to_date(date_string):
    return parse_datetime(date_string).strftime("%B %-d, %Y")

@register.simple_tag(takes_context=True)
def title_page_generator(context, path):
    title_page_en = "Low cost & No initial set-up cost. International SMS delivery service EZSMS"
    title_page_ja = "低価格、低コスト、初期費用なしの国内・国際ショートメッセージSMS配信サービスEZSMS"

    try:
        if 'en' in path:
            return title_page_en + " | " + path.split('/')[-2].replace("-", " ").capitalize()
        return title_page_ja + " | " + path.split('/')[-2].replace("-", " ").capitalize()

    except:
        if 'en' in path:
            return title_page_en
        return title_page_ja

@register.filter(name='latest_posts')
def latest_posts(queryset, number):
    return queryset[:number]
