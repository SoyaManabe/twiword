from django.shortcuts import render
from django.http import HttpResponse
from .sepjap import sep

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