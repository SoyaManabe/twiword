from django.shortcuts import render
from django.http import HttpResponse
from .sepjap import sep
from .models import Words

from social_django.models import UserSocialAuth

#indexは移動するかもしれません
def index(request):
    return render(request, 'collect_words/index.html')

def catch(request):
    texts='私はよく柿食う客だよ。'
    analyze = sep(texts)
    results = []
    for k, v in analyze:
        results.append(k)
    context = {
        'results': results[1],
    }
    print(results)
    return render(request, 'collect_words/catch.html',context)

def userhome(request, userurl):
    words = Words.objects.all()
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    print(user.access_token)
    context = {
        'words': words,
        'userurl': userurl,
        'user': user,
    }
    return render(request, 'collect_words/userhome.html', context)

def quiz(request, userurl):
    word = Words.objects.filter(user=userurl).order_by("?").first()
    context = {
        'word': word,
        'userurl': userurl,
    }
    return render(request, 'collect_words/quiz.html', context)

def wordlist(request, userurl):
    words = Words.objects.all()
    context = {
        'words': words,
        'userurl': userurl,
    }
    return render(request, 'collect_words/list.html', context)

def result(request, userurl):
    words = Words.objects.all()
    context = {
        'words': words,
        'userurl': userurl,
    }
    return render(request, 'collect_words/result.html', context)

