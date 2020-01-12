from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count

from .models import Post
from .forms import CommentForm, NewsletterForm, MessageForm



def index(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    new_newsletter = None
    if request.method == "POST":
        newsletter_form = NewsletterForm(data=request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            return redirect('index')
    else:
        newsletter_form = NewsletterForm()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])       

    paginator = Paginator(object_list, 4) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(p.num_pages)
    
    context = {
        "index": "active", # Adding active class to navbar
        'page': page, 
        'posts': posts, 
        'newsletter_form': newsletter_form,
        'tag': tag
        }
    return render(request, 'blog/index.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    
    session_key = 'viewed_post_{}'.format(post.pk)
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    comments = post.comments.filter(active=True)

    new_comment = None
    new_newsletter = None

    if request.method == 'POST':
        if request.POST.get("form_type") == 'newsletter': # form_type defined inside form as input tag in sidebar.html
            newsletter_form = NewsletterForm(data=request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                return redirect('index')
        elif request.POST.get("form_type") == 'add_comment': # form_type defined inside form as input tag in post_detail.html
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                return redirect('post_detail', year=year, month=month, day=day, post=post.slug)
    else:
        comment_form = CommentForm()
        newsletter_form = NewsletterForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'newsletter_form': newsletter_form,
        'similar_posts': similar_posts
    }
    return render(request, 'blog/post_detail.html', context)

def contact(request):
    new_message = None
    if request.method == 'POST':
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save()
            new_message.save()
            return redirect('contact')
    else:
        message_form = MessageForm()

    context = {
        "contact": "active", # Adding active class to navbar
        'message_form': message_form
    }

    return render(request, 'blog/contact.html', context)