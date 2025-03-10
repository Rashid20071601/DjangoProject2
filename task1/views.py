from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def main(request):
    return render(request, 'platform.html')


def choice(request):
    GAME = Game.objects.all()
    games = []

    for i in GAME:
        games.append({'title': i.title, 'description': i.description, 'cost': i.cost})

    context = {
        'buy': 'Купить',
        'games': games
    }
    return render(request, 'game.html', context)


def cart(request):
    return render(request, 'cart.html')


def sign_up(request):
    info = {}
    buyers = Buyer.objects.all()
    context = {
        'buyers': buyers
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        balance = request.POST.get('balance')
        age = request.POST.get('age')

        if not username or not balance or not age:
            info['error'] = "All fields are required."
        else:
            age = int(age)
            user_exists = Buyer.objects.filter(name=username).exists()

            if user_exists:
                info['error'] = "Username already exists."
            elif age < 18:
                info['error'] = "You must be at least 18 years old."
            else:
                Buyer.objects.create(name=username, balance=balance, age=age)
                info['success'] = f"Welcome, {username}!"

    context.update(info)

    return render(request, 'registration_page.html', context)


def news_list(request):
    # получаем все посты
    news = News.objects.all()

    # создаем пагинатор
    paginator = Paginator(news, 2)  # 2 поста на странице

    # получаем номер страницы, на которую переходит пользователь
    page_number = request.GET.get('page')

    # получаем посты для текущей страницы
    page_news = paginator.get_page(page_number)

    # передаем контекст в шаблон
    return render(request, 'news.html', {'page_news': page_news})