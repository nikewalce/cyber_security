from django.shortcuts import get_object_or_404, render

from .models import Article, Category


# список всех категорий
def category_list(request):
    categories = Category.objects.all()

    return render(
        request, "knowledge_base/category_list.html", {"categories": categories}
    )


# статьи внутри категории
def articles_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # выводим статьи в определенной категории
    articles = Article.objects.filter(category=category)

    return render(
        request,
        "knowledge_base/articles_by_category.html",
        {"category": category, "articles": articles},
    )


# детальная страница статьи
def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)

    return render(request, "knowledge_base/article_detail.html", {"article": article})
