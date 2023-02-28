from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinLengthValidator,validate_email,MinValueValidator,MaxValueValidator
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, NumericPasswordValidator
from account.validators import *

#회원 모델 생성
class Account(models.Model):
    #id,pw,name,e-mail,name,email,position,gisu

    POSITION = [
        ('OB', 'OB'),
        ('YB', 'YB'),
        ('O', 'Others')] # 디폴트는 Others로 설정

    TRACK = [
        ('B', 'Beginner'),
        ('C', 'Challenger')
    ]

    id = models.CharField(max_length=8,validators=[MinLengthValidator(5)],blank=False,unique=True, primary_key=True) #blank=False는 빈값을 허용하지 않겠다는 의미
    pw = models.TextField(max_length=300) # 회원가입 때 받은 값을 해싱된 값으로 저장
    name = models.CharField(max_length=5,validators=[MinLengthValidator(2),MaxValueValidator(8)],blank=False)
    email = models.EmailField(unique=True, validators=[validate_email]) # validator 오류
    student_id = models.PositiveSmallIntegerField(validators=[MinValueValidator(1000000),MaxValueValidator(2399999)])
    major = models.TextField(max_length=15)
    position = models.CharField(max_length=2, choices=POSITION, default='O')
    track = models.CharField(max_length=1,choices=TRACK)
    gisu = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(11)],null=True)

    def __str__(self):
        return self.id

    def is_valid(validation, self):
        # 클라이언트단 유효성 검사 통과 (임시) -> 프론트 form에서 hidden으로 넘겨주시면 될 듯 합니다.
        if validation != 'valid':  # 임시 코드
            # 프론트 유효성 검사에서 실패한 경우 회원가입 페이지로 리다이렉트
            # 실시간으로 빨간 에러 뜨는 것은 공부해보아야 할 것 같습니다.
            return False

    # 서버측 유효성 검사

        # 아이디 중복 검사
        if user_exists(self.id):
            return False

        # 이메일 중복 검사
        if email_exists(self.email):
            print("이미 가입된 아이디입니다." #프론트로 전달
            return False

        # 비밀번호 유효성 검사
        try:
            pw_validators = [
                MinimumLengthValidator(min_length=8),
                NumericPasswordValidator,
            ]
            # 길이 및 숫자 암호 아닌지 검사
            # 특수 기호 검사는 좀 후에.........
            validate_password(self.pw,pw_validators)

        except ValidationError:
            return False

