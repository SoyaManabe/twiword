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
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

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
        numberOfCompleted = words.filter(quiz=False).count()
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
            if request.POST.get("delete") == "True":
                    word = Words.objects.get(id=int(wordId))
                    word.delete()
                    words = Words.objects.filter(owner=userurl)
                    context = {
                        'words': words,
                        'userurl': userurl,
                        'user': user,
                    }
                    return render(request, 'collect_words/list.html', context)
            else:
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
        context = {
            'words': words,
            'userurl': userurl,
            'results': results,
        }
        return render(request, 'collect_words/result.html', context)
    else:
        return errorlog()

@login_required
def extract(request, userurl):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    if permittion(user, userurl):
        if request.method == "POST":
            if request.POST.get("add")=="True":
                separated_word = request.POST.get("separated_word")
                query = {
                    'Dic':'EJdict',
                    'Word':separated_word,
                    'Scope':'HEADWORD',
                    'Match':'STARTWITH',
                    'Merge':'AND',
                    'Prof':'XHTML',
                    'PageSize':'1',
                    'PageIndex':'0',
                }
                p = urllib.parse.urlencode(query)
                url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite?' + p
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    xml_string = response.read()
                root = ET.fromstring(xml_string)
                print(root[1].text)
                if int(root[1].text) == 0:
                    return HttpResponse("No word found")
                else:
                    dictId = root[3][0][0].text
                    params = {
                        'Dic':'EJdict',
                        'Item':dictId,
                        'Prof':'XHTML',
                        'Loc':'',
                    }
                    p = urllib.parse.urlencode(params)
                    url = 'http://public.dejizo.jp/NetDicV09.asmx/GetDicItemLite?' + p
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        xml_string = response.read()
                    root = ET.fromstring(xml_string)
                    trans = root[2][0][0].text
                    text = request.POST.get("text")
                    user = Users.objects.get(id=request.user.id)
                    Words.objects.create(user=user,
                                        tweet=text,
                                        word=separated_word,
                                        trans=trans,
                                        owner=userurl,
                                        )
                    name = request.POST.get("name")
                    profile_image_url = request.POST.get("profile_image_url", "")
                    separated_words = language(text)
                    for i in range(len(separated_words)):
                        if Words.objects.filter(word=separated_words[i]).exists():
                            separated_words[i] = "."
                    context = {
                        'name': name,
                        'profile_image_url': profile_image_url,
                        'text': text,
                        'separated_words': separated_words,
                        'userurl': userurl,
                    }
                    return render(request, 'collect_words/extract.html', context)
            else:
                name = request.POST.get("name")
                profile_image_url = request.POST.get("profile_image_url", "")
                text = request.POST.get("text", "")
                separated_words = language(text)
                for i in range(len(separated_words)):
                    if Words.objects.filter(word=separated_words[i]).exists():
                        separated_words[i] = "."
                context = {
                    'name': name,
                    'profile_image_url': profile_image_url,
                    'text': text,
                    'separated_words': separated_words,
                    'userurl': userurl,
                }
                return render(request, 'collect_words/extract.html', context)
        else:
            return errorlog()
    else:
        return errorlog()

def permittion(user, userurl):
    if not user.access_token["user_id"] == str(userurl):
        return False
    else:
        return True

def errorlog():
    return HttpResponse("ERROR")

def translate(word):
    url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'
    query = {
        'Dic':'EJdict',
        'Word':'infinity',
        'Scope':'HEADWORD',
        'Match':'STARTWITH',
        'Merge':'AND',
        'Prof':'XHTML',
        'PageSize':'1',
        'PageIndex':'0',
    }
    r = request.get(url, params=query)
    print("response", r.json())
    return ""