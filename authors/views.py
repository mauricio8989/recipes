from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm, LogInForm
from django.contrib import messages


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        "is_detail_page": True,
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Registration successful')

        del request.session['register_form_data']

    return redirect('authors:register')


def login_view(request):
    form = LogInForm()
    return render(request, 'authors/pages/login_view.html', context={
        'form': form,
        "is_detail_page": True,
    })
