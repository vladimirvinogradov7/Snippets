from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegisterForm
from django.contrib.auth.decorators import login_required


def get_base_context(request, pagename):
    return {
        'pagename': pagename
    }


def index_page(request):
    context = get_base_context(request, 'PythonBin')
    return render(request, 'pages/index.html', context)


@login_required
def add_snippet_page(request):
    if request.method == "GET":
        context = get_base_context(request, 'Добавление нового сниппета')
        form = SnippetForm()
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
        return redirect('snippets-list')


def snippets(request):
    snippets = Snippet.objects.filter(public=True)
    context = get_base_context(request, 'Просмотр сниппетов')
    context['page_description'] = "Все публичные сниппеты всех пользователей"
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    context = get_base_context(request, 'Страница сниппета')
    context["snippet"] = snippet
    return render(request, 'pages/snippet_page.html', context)


@login_required
def snippets_my(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = get_base_context(request, 'Мои сниппеты')
    context['page_description'] = "Все сниппеты созданные вами"
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


def snippets_delete(request, id):
    snippet = Snippet.objects.get(id=id)
    snippet.delete()
    return redirect('snippets-list')


def snippets_edit(request, id):
    if request.method == "GET":
        context = get_base_context(request, 'Редактирование нового сниппета')
        snippet = Snippet.objects.get(id=id)
        form = SnippetForm(instance=snippet)
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        snippet = Snippet.objects.get(id=id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippets-list')


def register(request):
    if request.method == "GET":
        context = get_base_context(request, 'Регистрация пользователя')
        form = UserRegisterForm()
        context["form"] = form
        return render(request, 'pages/registration.html', context)
    if request.method == "POST":
        context = get_base_context(request, 'Регистрация пользователя')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('home')
        #  Если данные регистрации невалидны
        context["form"] = form
        return render(request, 'pages/registration.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        errors = ["Неверные логин и/или пароль", ]
        context = get_base_context(request, "PythonBin")
        context['errors'] = errors
        context['username'] = username
        return render(request, 'pages/index.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')