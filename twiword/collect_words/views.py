from django.shortcuts import render
from django.http import HttpResponse
from .sepjap import sep
from .models import Words
from .models import Users
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from .collect import collect, userImg
from .lanproc import language

#indexは移動するかもしれません
@login_required
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    userurl = user.access_token['user_id']
    #return render(request,'user_auth/top.html', {'user': user})
    context = {
        'user':user,
        'userurl': userurl,
    }
    return render(request,'user_auth/top.html', context)

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

@login_required
def userhome(request, userurl):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    if permittion(user, userurl):
        register = Users.objects.filter(userId=user.access_token['user_id'])
        if not register:
            imgUrl = userImg(user.access_token['screen_name'])
            newUser = Users.objects.create(screenName=user.access_token['screen_name'],
                                   userId=user.access_token['user_id'],
                                   imgUrl=imgUrl, 
                                   )
        register = Users.objects.get(userId=user.access_token['user_id'])
        words = Words.objects.filter(owner=user.access_token['user_id'])
        numberOfWords = words.count()
        numberOfCompleted = words.filter(quiz=True).count()
        if numberOfWords:
            percentageOfProgress = round(numberOfCompleted / numberOfWords * 100, 2)
        else:
            percentageOfProgress = 'N/A'
        context = {
            'words': words,
            'userurl': userurl,
            'user': user,
            'register': register,
            'numberOfWords': numberOfWords,
            'percentageOfProgress': percentageOfProgress,
            
        }
        return render(request, 'collect_words/userhome.html', context)
    else:
        return errorlog()

@login_required
def quiz(request, userurl):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    if permittion(user, userurl):
        if request.method == "POST":
            wordId = request.POST.get("wordId", "")
            word = Words.objects.get(id=int(wordId))
            word.quiz = False
            word.save()
            #word = Words.objects.filter(owner=user.access_token['user_id'],quiz=True).order_by("?").first()
            word = Words.objects.filter(owner=userurl, quiz=True).order_by("?").first()
            context = {
                'word': word,
                'userurl': userurl,
            }
            return render(request, 'collect_words/quiz.html', context)
        if request.method == "GET":
            #word = Words.objects.filter(owner=user.access_token['user_id'], quiz=True).order_by("?").first()
            word = Words.objects.filter(owner=userurl, quiz=True).order_by("?").first()
            context = {
                'word': word,
                'userurl': userurl,
            }
            return render(request, 'collect_words/quiz.html', context)
    else:
        return errorlog()

@login_required
def wordlist(request, userurl):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    if permittion(user, userurl):
        if request.method == "POST":
            wordId = request.POST.get("wordId", "")
            word = Words.objects.get(id=int(wordId))
            word.quiz = not(word.quiz)
            word.save()
            #words = Words.objects.filter(owner=user.access_token['user_id'])
            words = Words.objects.filter(owner=userurl)
            context = {
                'words': words,
                'userurl': userurl,
                'user': user,
            }
            return render(request, 'collect_words/list.html', context)
        if request.method == "GET":
            #words = Words.objects.filter(owner=user.access_token['user_id'])
            words = Words.objects.filter(owner=userurl)
            context = {
                'words': words,
                'userurl': userurl,
                'user': user,
            }
            return render(request, 'collect_words/list.html', context)
    else:
        return errorlog()

@login_required
def result(request, userurl):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    if permittion(user, userurl):
        words = Words.objects.all()
        newlist = []
        screenName = user.access_token['screen_name']
        results = collect(screenName, newlist)
        for result in results:
            processes = language(result)
            
        context = {
            'words': words,
            'userurl': userurl,
            'results': results,
        }
        return render(request, 'collect_words/result.html', context)
    else:
        return errorlog()

def permittion(user, userurl):
    if not user.access_token["user_id"] == str(userurl):
        return False
    else:
        return True

def errorlog():
    return HttpResponse("ERROR")