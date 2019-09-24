from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, EmailPostForm, CommentPostForm
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail


#  replaced with object View
# def post_list(request):
#     objects = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     paginator = Paginator(objects, 3) #3 posts each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post_list.html', {'posts': posts, 'page': page})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post_list.html'

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Queryset of active comments
    comments = Comment.objects.filter(active=True)
    if request.method == 'POST':
        # A comment was postd
        comment_form = CommentPostForm(request.POST)
        if comment_form.is_valid():
    #         Create comment object but don't save to db yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentPostForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments':comments, 'comment_form':comment_form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form= PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url,cd['name'],cd['comment'])
            send_mail(subject,message,'retip1994@wp.pl',[cd['to']])
            sent = True
    #             ...send Email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html',{'post':post,'form':form, 'sent':sent})



