from django.shortcuts import render, redirect, reverse, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .decorators import *
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

base_url = 'http://127.0.0.1:8000/'

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Company.objects.create(
                user=user,
                name=user.username,
            )
            messages.success(request, 'Account was created for ' + username)

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# @unauthenticated_user
def loginPage(request):
    form = UserCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            company_id = request.user.company.id
            return redirect('user/' + str(company_id) + '/')
        else:
            messages.info(request, 'Username or Password was incorrect')
            render(request, '', context)

    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)

    return redirect('')

def userPage(request, pk):
    company = Company.objects.get(id=pk)
    questions = request.user.company.question_set.all()
    context = {'questions': questions, 'company': company}

    return render(request, 'accounts/user.html', context)

# @login_required(login_url='login')
def addQuestion(request, pk):
    company = Company.objects.get(id=pk)
    form = QuestionForm(initial={'company': company}, instance=company)

    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/addQuestion.html', context)

def candidateLogin(request, pk, token):
    company = Company.objects.get(id=pk)
    token_db = Token.objects.get(user=company.user)
    print(token)
    print(token_db)
    if str(token_db) == str(token):
        form = CreateCandidateForm(initial={'company': company}, instance=company)
        context = {'form': form, 'company': company}
        if request.method == 'POST':
            form = CreateCandidateForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                Candidate.objects.create(
                    user=user,
                    name=user.username,
                    company=company,
                )
                return redirect('/candidatePage.html')
        return render(request, 'accounts/candidateLogin.html/', context)
    else:
        return render(request, 'accounts/candidateLoginFailed.html/')

def candidatePage(request, pk_comp, pk_cand, pk_quest):
    company = Company.objects.get(id=pk_comp)
    question = Question.objects.get(id=pk_quest)
    candidate = Candidate.objects.get(id=pk_cand)
    form = SubmitAnswer(initial={'question': question, 'candidate': candidate})
    if request.method == 'POST':
        form = SubmitAnswer(request.POST)
        if form.is_valid():
            form.save()

    return redirect('/candidatePage/' + str(pk_comp) + '/' + str(pk_cand), str(pk_quest))

def invite(request, pk):
    company = Company.objects.get(id=pk)
    form = CandidateEmailForm()
    if request.method == 'POST':
        form = CandidateEmailForm(request.POST)
        if form.is_valid():
            account = form.save()
            print(company.user)
            token = Token.objects.get(user=company.user)
            print(token)
            send_mail('Hello!!!', 'The login URL is the following: \n' + base_url + str('candidateLogin/') + str(pk) + str('/') + str(token), 'myinterview.sample@gmail.com',
            [account.email], fail_silently=False)

    context = {'form': form}
    return render(request, 'accounts/index.html', context)