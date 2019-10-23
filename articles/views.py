from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Article, Comment
from IPython import embed
from django.http import HttpResponse

# Create your views here.

#@login_required(login_url='user/login.html')
@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user_id = request.user.id
            article.save()
            return redirect('articles:detail', article.pk)

        # Article 을 생성해달라고 하는 요청
        
    else: #GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()

    context = {'form': form}
    return render(request, 'articles/create.html', context)

@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    

    return render(request, 'articles/index.html', context)

@require_GET
def detail(request, article_pk):
    # 사용자가 url 에 적어보낸 article_pk를 통해 디테일 페이지를 보여준다.
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()
    form = CommentForm()
    context = {'article': article, 'comments': comments, 'form': form}

    return render(request, 'articles/detail.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
            pass
        
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {'form': form}
    return render(request, 'articles/update.html', context)


# @login_required login페이지에서 nextpage로 보내봣자 get요청이라 post로 막힌다.
@require_POST
def delete(request, article_pk):
    # article_pk에 맞는 article 을 꺼낸다.
    # 삭제한다.
    if request.user.is_authenticated:

        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    return redirect('articles:index')
    
@login_required    
@require_POST
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # temp.article = article
    form = CommentForm(request.POST)
    if form.is_valid():
        
        comment = form.save(commit=False)
        comment.article_id = article_pk
        comment.user_id = request.user.id
        comment.save()

    return redirect('articles:detail', article_pk)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    
    if request.user.is_authenticated:
        
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
            return redirect('articles:detail', article_pk)
    return HttpResponse('로그인을 하세요', status=401)

def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    if article.liked_users.filter(pk=user.pk).exists():
        user.liked_articles.remove(article)
    else:
        user.liked_articles.add(article)
    print(article.liked_users.all())
    return redirect('articles:detail', article_pk)

def follow(reqeust, article_pk, user_pk):
    # 로그인한 유저가 게시글 유저를 Follow or Unfollow 한다.
    user = reqeust.user
    person = get_object_or_404(get_user_model(), pk=user_pk) # 게시글 주인

    if user in person.followers.all():
        person.followers.remove(user)
    else:
        person.followers.add(user)

    return redirect('articles:detail', article_pk)