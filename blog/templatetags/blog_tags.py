from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def each_tag_count(tag_name=""):
    return Post.published.all().filter(tags__in=[tag_name]).count()

@register.inclusion_tag('blog/includes/categories.html')
def show_total_tags():
    total_tags = Post.tags.all()
    return {'total_tags': total_tags}

@register.inclusion_tag('blog/includes/popular_posts.html')
def show_popular_posts(count=3):
    popular_posts = Post.published.order_by('-views')[:count]
    return {'popular_posts': popular_posts}

@register.inclusion_tag('blog/includes/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))