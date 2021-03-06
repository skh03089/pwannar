from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Article, Tag
from .forms import ArticleForm, CommentForm


def MainPage(request):
    return render(request, 'mainpage.html')


@login_required
def board_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST or None)
    ctx = {
        'article': article,
        'comment_form': comment_form,
        'pk': pk,
        'did_like_article': article.liker_set.filter(pk=request.user.pk),
    }

    if request.method == "POST" and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.author = request.user
        new_comment.save()
        return redirect(article.get_absolute_url())

    return render(request, 'board_detail.html', ctx)


def board_list(request, tag_pk=None):
    if tag_pk is not None:
        article_list = Article.objects.filter(tag__pk=tag_pk)
        try:
            tag = Tag.objects.get(pk=tag_pk)
        except Tag.DoesNotExist:
            raise Http404('없는 Tag입니다.')
    else:
        article_list = Article.objects.all()
        tag = None

    ctx = {
        'board_list': article_list,
        'tag_list': Tag.objects.all(),
        'tag_selected': tag,
    }

    return render(request, 'board_list.html', ctx)


@login_required
def board_create(request):
    form = ArticleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
            article = form.save()

            return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'board_create.html', ctx)


def board_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        article = form.save()
        return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'board_create.html', ctx)


@login_required
def board_delete(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect(reverse('core:board_list'))
    else:
        return HttpResponse(status=400)


@login_required
def article_like(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        if request.user.liked_article_set.filter(pk=pk).exists():
            article.liker_set.remove(request.user)
        else:
            article.liker_set.add(request.user)
        return redirect(article.get_absolute_url())
    else:
        return HttpResponse(status=400)
