from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from .forms import CommentForm


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = context['category'].posts.all()
        categories = [cat for cat in Category.objects.all() if cat.posts.exists()]
        context['categories'] = categories
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = [cat for cat in Category.objects.all() if cat.posts.exists()]
        context['categories'] = categories
        news = Category.objects.get(slug='novosti').posts.all()[:3]
        context['news'] = news
        return context

# class PostDetail(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     slug_url_kwarg = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         comments = context['post'].comments.filter(active=True)
#         new_comment = None
#         if self.request.method == 'POST':
#             comment_form = CommentForm(data=self.request.POST)
#             if comment_form.is_valid():
#                 new_comment = comment_form.save(commit=False)
#                 new_comment.post = context['post']
#                 new_comment.save()
#         else:
#             comment_form = CommentForm()
#         context['comments'] = comments
#         context['new_comment'] = new_comment
#         context['comment_form'] = comment_form
#         return context


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    total_comments = comments.count()
    categories = [cat for cat in Category.objects.all() if cat.posts.exists()]
    news = Category.objects.get(slug='novosti').posts.all()[:3]
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'news': news,
                   'comments': comments,
                   'categories': categories,
                   'new_comment': new_comment,
                   'total_comments': total_comments,
                   'comment_form': comment_form})
