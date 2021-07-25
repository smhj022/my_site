from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

############## methods for statting page ##############

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })


# class StartingPageView(TemplateView):
#     template_name = "blog/index.html"
#    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         latest_posts = Post.objects.all().order_by("-date")[:3]
#         context["posts"] = latest_posts
#         return context

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

##################### end startingpage ####################

########### Three methods for post ###########

# method 1 : using function only 

# def posts(request):
#     return render(request, "blog/all_posts.html", {
#         "all_posts": Post.objects.all()
#     })

# method 2 : using class based template view

# class PostsView(TemplateView):
#     template_name = "blog/all_posts.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["all_posts"] = Post.objects.all()
#         return context

# method 3 : using class based List view 


class PostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    context_object_name = "all_posts"


################# end posts ####################


def post_detail(request, slug):
    show_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
        "view_post": show_post,
        "tags": show_post.tags.all()

    })


# class PostDetailsView(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tags"] = self.objects.tags.all()
#         return context