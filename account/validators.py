from django.core.exceptions import ValidationError, ObjectDoesNotExist
from account.models import Account
import re

def is_pw_same(pw1,pw2): # 비밀번호 이중 확인 코드
    return True if pw1 == pw2 else False

"""def id_validator(value):
    # 5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능
    len_val=len(value)>=5 and len(value)<=20
    punct_val=True
    punct=re.compile("a-zA-Z0-9_-") #a-zA-Z0-9_- 제외한 기호들
    for c in value:
        if punct.match(c) is None:
            punct_val=False
            break
    if not len_val or not punct_val:
        raise ValidationError("5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.")
"""
def user_exists(input_id): # 아이디 존재 검사, ajax로 구현
    if Account.objects.filter(id=input_id).exists():
        return True
    else: return False

def email_exists(input_email): #이메일 존재 검사, ajax로 구현
    if Account.objects.filter(email=input_email).exists():
        return True
    else: return False

