from django import template
from ..models import Post,Comment
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_date():
    return Post.published.last().publish

@register.inclusion_tag("partials/latest_post.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts':l_posts
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
