from django.shortcuts import render, get_object_or_404
from .models import Post



def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })


def posts(request):
    return render(request, "blog/all_posts.html", {
        "all_posts": Post.objects.all()
    })


def post_detail(request, slug):
    show_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
        "view_post": show_post,
        "tags": show_post.tags.all()

    })
