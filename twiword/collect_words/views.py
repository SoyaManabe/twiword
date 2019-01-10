from django.shortcuts import render
from django.http import HttpResponse
from .sepjap import sep

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

def userhome(request):
    return render(request, 'collect_words/userhome.html')

def quiz(request):
    return render(request, 'collect_words/quiz.html')

def wordlist(request):
    return render(request, 'collect_words/list.html')

def result(request):
    return render(request, 'collect_words/result.html')

