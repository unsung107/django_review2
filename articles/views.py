from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.views.decorators.http import require_POST, require_GET
from .models import Article

# Create your views here.


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

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
    context = {'article': article}
    return render(request, 'articles/detail.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
        pass
    
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'articles/update.html', context)

@require_POST
def delete(request, article_pk):
    # article_pk에 맞는 article 을 꺼낸다.
    # 삭제한다.
    
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')
    

    pass
    
    