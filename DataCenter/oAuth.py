from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect
from rest_framework import permissions
from DataCenter.settings import SECRET_KEY, OAUTH_URL
from django.views.decorators.csrf import csrf_exempt
import jwt, time
import json
import requests

class TokenAuthentication(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.session.get('token', False)
        print(token)
        verify_token_url = OAUTH_URL + '/api/verify_token/'

        if token:
            data = {
                'token': token
            }
            r = requests.post(url=verify_token_url, data=data)
            print(r.json())
            print(r.status_code)
            if r.status_code == 200:
                return True
            else:
                return False
        else:
            print('TokenAuthentication False, Token Null.')
            return False

def logout(request):
    request.session['username'] = None
    request.session['token'] = None
    StatusDict = {'status':'logout','statusinfo':'您已成功退出！'}
    return redirect('/')

@csrf_exempt
def login(request):
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    postBody = request.body
    json_result = json.loads(postBody)
    username = json_result['username']
    password = json_result['password']
    data = {
        'username': username,
        'password': password
    }
    print(data)
    login_url = OAUTH_URL + '/api/login/'
    res = requests.post(url=login_url, data=data)
    print(res.json())
    print(res.status_code)
    if res.status_code == 200:
        request.session['username'] = username
        request.session['token'] = res.json()['token']
        return JsonResponse(res.json())
    else:
        return HttpResponse("Authentication False", status=401)

def token_check(request):
    token = request.session.get('token', False)
    print(token)
    verify_token_url = OAUTH_URL + '/api/verify_token/'

    if token:
        data = {
            'token': token
        }
        print('start authentication............')
        print(time.time())
        r = requests.post(url=verify_token_url, data=data)
        print(time.time())
        print(r.status_code)
        if r.status_code == 200:
            return HttpResponse("TokenAuthentication True", status=200)
    else:
        return HttpResponse("TokenAuthentication False", status=401)
