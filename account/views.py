from django.shortcuts import HttpResponse,render,redirect
from django.http import JsonResponse
from argon2 import PasswordHasher
import json
from account.models import Account

#회원가입
#ajax로 회원가입 폼 만들자..............ㅠ ㅠ ㅠ
#id 중복 검사 아마 버튼 누르면 post로 연결되는듯 하다 ajax 이용하는듯


def temp_index(request):
    return HttpResponse("""
    <html>
        <body>
            <h1> Temporary site </h1>
            </br>
            <a href='/signup'>signup
        </body>
    </html>
    """)


def is_ID_Exists(request):
    id=request.POST.get(id)
    if not Account.objects.filter(id=id): #아이디가 없는 경우
        return False
    else:
        return True

def sign_up(request):
    if request.method()=='GET':
       return render("회원가입 템플릿 파일~",request)
    elif request.method()=='POST':
        res_data = []  # 회원가입할 때 일어나는 오류를 res_data라는 딕셔너리에 담음.
        if not is_ID_Exists(request): #id 가 없는 경우
            if request.POST.get('pw') != request.POST.get('re_pw'): #pw 두번 입력한게 일치하면
                res_data['error']="비밀번호가 일치하지 않습니다."
                return render("회원가입 템플릿 파일",request,res_data)
                #res_data에 담긴 오류를 html코드 로그인 아래에 빨간 글씨로 출력
            else:
                pw=PasswordHasher(request.POST.get('pw')) #argon2 PasswordHasher로 encrypt
                email = request.POST.get('e-mail')
                new_acc=Account(id,pw,email)
                #validation은 어떻게 추가시켜주어야할지 찾기
                new_acc.save()
                return render('login') #로그인 페이지로 이동. 위에 회원가입 완료되었다고 출력하기
    else:
                # 유효하지 않은 경우
                return render('로그인 페이지') #오류코드랑 로그인 페이지 출력


def login(request):
    if request.method() == 'GET': #로그인폼 페이지로 이동~~~~~~~
        print()
    elif request.method() == 'POST':
        id=request.POST.get('id')
        pw=request.POST.get('pw')

        if is_ID_Exists(request) and PasswordHasher().verify(Account.objects.get(id=id).pw, pw):
            #세션 생성 및 쿠키 세팅~~~~~~~
            #루트페이지로 리다이렉트
            return redirect('')
        else: #아이디가 혹은 비밀번호가 틀리면
            res_data = []
            res_data["error"] = "아이디 혹은 비밀번호를 다시 입력하세요."
            return render('login',res_data)


def verifyPassword(request):
    id=request.session['user_id']
    if request.method=='GET':
        return render('비밀번호 체크하는 페이지',id)
    elif request.method=='POST':
        # 비밀 번호가 올바른 경우
        # 비밀 번호가 틀린 경우
        res_data=[]
        res_data['error']="비밀번호가 틀립니다."
        return render('비밀번호 체크하는 페이지',res_data, id)
    #기존 페이지가 업데이트면 updateUser로 이동, 탈퇴면 deleteUser로 이동

def updateUser(request):
    id = request.session['user_id']
    user=Account.objects.get(id=id)
    return render("수정 페이지")
    #폼에 placeholder로 사용자 정보 띄워주기

def deleteUser(request):
    id = request.session['user_id']
    user = Account.objects.get(id=id)
    user.delete()
    return HttpResponse("후잉 잘가 ㅠㅠ.html")