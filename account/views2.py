from django.shortcuts import HttpResponse,render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import json
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


def sign_up(request):
    if request.method == 'GET':
        return render(request,'signup.html')

    elif request.method == 'POST':

        # id,pw,email,이름,학번,학과,전공,포지션
        try:
            id=request.POST.get('id') # id
            pw=make_password((request.POST.get('pw1'))) # 패스워드 암호화
            name=request.POST.get('name') # 이름
            email = request.POST.get('email')  # 이메일
            student_id=int(request.POST.get('student_id')) # 학번
            major=request.POST.get('major') # 전공
            position=request.POST.get('status') # YB,OB, 외부인
            validation=request.POST.get('validation') # 프론트 단 유효성 검사 통과

            if position == 'O': # 포지션이 Others인 경우
                user = Account(id, pw, email, name, student_id, major, position)
                if Account.is_valid(validation,user):
                    user.save()

            elif position == 'OB' or 'YB': # 동아리원인 경우 트랙 및 기수를 폼에서 입력받는다.
                track=request.POST.get('track') # 트랙
                gisu=request.POST.get('gisu') # 기수
                user = Account(id, pw, email, name, student_id, major, position, track, gisu)
                if Account.is_valid(validation,user):
                    user.save()
            else:
                raise Exception

        except ValidationError:
            print("Validation Error on Server")
            return render(request,'signup.html')

        except Exception as e:
            return render(request,'signup.html')
