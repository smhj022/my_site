from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .form import CommentForm
from .models import Comments, Post

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


class PostDetails(View):
    def is_stored(self, request, post_id):
        stored_post = request.session.get("stored_post")
        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        show_post = get_object_or_404(Post, slug=slug)
        form = CommentForm()
        comment_on_post = Comments.objects.filter(post_id=show_post.id)

        return render(request, "blog/post-detail.html", {
            "view_post": show_post,
            "tags": show_post.tags.all(),
            "comment_from": form,
            "comments": comment_on_post.order_by("-id"),
            "saved_for_later": self.is_stored(request, show_post.id)
        })

    def post(self, request, slug):
        show_post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # important : As post is not part of form we need to add post in form as given
            comment = comment_form.save(commit=False)
            comment.post = show_post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[show_post.slug]))

        return render(request, "blog/post-detail.html", {
            "view_post": show_post,
            "tags": show_post.tags.all(),
            "comment_from": comment_form,
            "comments": show_post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored(request, show_post.id)
        })

# class PostDetailsView(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tags"] = self.objects.tags.all()
#         return context


class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_post")
        
        context = {}

        if stored_post is None:
            context["posts"] = []
            context["has_post"] = False
        else:
            post = Post.objects.filter(id__in=stored_post)
            context["posts"] = post
            context["has_post"] = True
        return render(request, "blog/stored-post.html", context)

    def post(self, request):
        # get data from session
        stored_post = request.session.get("stored_post")

        # If on stored post before we create a stored_post list
        if stored_post is None:
            stored_post = []

        # getting post id from the request.POST 
        post_id = int(request.POST["post_id"])

        # if post_id already in stored_post then then leave it otherwise add post id to the session
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
            
        ## saving data to the session
        request.session["stored_post"] = stored_post
        return HttpResponseRedirect("/")
