from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

people = [{"name": "Hannah", "age": 23, "gender": "Female", "pw" : 1234},
          {"name": "Jihyeon", "age":23,"gender":"Female", "pw": 2549},
          {"name": "Minji", "age":23, "gender":"Female","pw":1212},
          {"name": "Seona","age":23,"gender":"Female","pw":1213}]

def index(request):
    article = "<h2>Welcome</h2> Sign up! :)"
    return HttpResponse(HTML_template(article,request))

/use
@csrf_exempt
def HTML_template(article,request=None):
    # 제목, 회원 검색, 리스트 -> 회원 상세정보 페이지로 이동
    # 회원 가입, 밑에 소개글

    global people

    person_list = ""
    for person in people:
        person_list += f"""<li><a href='/read/{person["name"]}'>{person["name"]}</a></li>"""

    # redirect 기능 수정 필요 -> 해결
    search = f'''
                  <form action='/read/search'>
                      <h3>Search user info with user name:</h3> 
                      <input type='text' name=input_name> <input type='submit' value='Enter'></h3>
                  </form>
              '''

    # input_name 있는지 없는지로 얘가 검색 타고 들어왔는지 아닌지를 구분.
    #if request.GET["input_name"] != None:
        #return redirect(f'read/{request.GET.get("input_name")}')
    #if not request.GET.keys():
    #    print(request.GET)
    #   for key in request.GET.keys():
    #       if key == "input_name":
    #            return redirect(f'read/{request.GET.get("input_name")}')
    #GET 딕셔너리가 비어있는 경우(즉, 아무 파라미터도 받지 못한 경우)
    return f"""
                <html>
                        <body>
                            <h1><a href='/'>Hannah and her friends</a></h1>
                            {article}
                            {search}
                            <h3>Friend List</h3>
                            <ol>{person_list}</ol>
                           
                            </br>
                            <a href='/sign_up'><input type='submit' value='Sign Up'></a> <a href='/update'><input type='submit' value='Update'></a>
                            <input type='hidden' name='update' > <a href='/login/delete'><input type='submit' value='Delete'>
                        </body>
                </html>
                """

        #return redirect('') 리다이렉트가 왜 안되누.. get mothod이므로 리다이렉트해도 받은 파라미터는 강제로 뒤로 딸려오는듯...

# 비밀번호 기능 구현 후 비밀번호 같아야지만 수정할 수 있게 하기.
# 숫자 4자리로만 이루어져있도록 하기
@csrf_exempt
def sign_up(request):
    form_script = f"""
            <html>
                <body>
                    <h1><a href='/'>Hannah and her friends</a></h1>
                    <fieldset> 
                        <legend>Sign-up</legend>
                            <form action='/sign_up' method='POST'>              
                                <p><b>Name</b> : <input type='text' placeholder='name' name='name'></p>
                                <p><b>Password</b> : <input type='password' name='pw'> (Only 4 numbers are allowed!)</p>
                                </hr> 
                                <p><b>Age</b>  : <input type='text' placeholder='age' name='age'></p>
                                <p><b>Gender</b>:      
                                         <input type='radio' name='gender' value='Male'>Male 
                                         <input type='radio' name='gender' value='Female'>Female<p>
                                <input type='submit' value='submit'>
                            </form>
                    </fieldset>    
                </body>
            <html>
            """
    if request.method == 'GET':
        return HttpResponse(form_script)

    elif request.method == 'POST':
        global people
        if (type(int(request.POST.get("pw"))) is int) and len(request.POST.get("pw")) == 4:
            # 비밀번호가 숫자 4자리인 경우 통과
            # POST에서 key-value의 value는 숫자여도 string으로 반환된다.
            # type() -> 자료형 확인 함수

            people.append({"name":request.POST.get("name"),
                           "age":request.POST.get("age"),
                           "gender":request.POST.get("gender"),
                           "pw":int(request.POST.get("pw"))})
            return redirect(f'read/{request.POST.get("name")}')

        else :
            # 비밀번호가 숫자 4자리가 아닌 경우 경고메시지 출력 후 다시 입력하게함
            warning_message="Check your password!"
            return HttpResponse(form_script+"\n "+warning_message)

def read(request,name):
    #회원 정보 페이지
    search_name=request.GET.get("input_name")
    article=''
    global people
    if search_name is None :
        for person in people:
            if name == person["name"]:
                person_info = person
                article=f"""
                    <h2>{person_info["name"]}</h2>
                    <ul>
                    <li>Name : {person_info["name"]}</li>
                    <li>Age : {person_info["age"]}</li>
                    <li>Gender : {person_info["gender"]}</li>
                </ul>
            """
        return HttpResponse(HTML_template(article,request))

    else :
        for person in people:
            if search_name in person['name']:
                return redirect(f'/read/{search_name}')

        return HttpResponse(HTML_template("No user found. Sign up!"))



#login/login으로 되는 문제 해결해야함...
@csrf_exempt
def login(request,next):
    #로그인 틀리면 틀렸다고 출력하고 로그인페이지 그대로
    #로그인 맞으면 이전 페이지가 뭐였냐에 따라 다른 페이지로 이동.
    global people
    login_form=f"""
            <html>
                <body>
                <h1><a href='/'>Hannah and her friends</a></h1>
                <h2>LOGIN</h2>
                    <fieldset>
                        <legend>Login</legend>
                        <form action='/login/{next}' method='POST'>
                        <input type=hidden name=next value={next}>
                        <p>Name : <input type='text' name='name'></p>
                        <p>PW : <input type='password' name='pw'></p>
                        <p><input type='submit' value='login'></p>
                        </form>
                    </fieldset>
                </body>
            </html>
        """
    if request.method == 'GET':
        return HttpResponse(login_form)
    elif request.method == 'POST':
        input_name=request.POST.get("name") #로그인했을 때 입력받은 아이디
        for person in people:

            if input_name == person["name"]:
                # 아이디 비번 다 맞음
                    if int(request.POST.get("pw")) == person["pw"]:
                        if next=='update_info':
                            return redirect(f'/update/{input_name}')
                        elif next =='delete':
                            return redirect(f"/delete/{input_name}")
                    else: # 아이디는 있는데 비밀번호가 틀린 경우
                        return HttpResponse(login_form+"\n Wrong Password!")
        #반복문 빠져나온 경우(아이디 없는 경우)
        return HttpResponse(login_form + " \n No user found.")



@csrf_exempt
def update_login(request):
    #로그인화면으로 이동 후 update하는 개인정보 수정 페이지로 이동시키기
    #GET으로 파라미터 전달해주기

    next='/update_info'
    #아이디나 비번 틀린 경우 처리
    return redirect('/login'+next)

@csrf_exempt
def update_info(request,name):
    #로그인 화면에서 넘어옴
    global people
    person_dict={}
    for person in people:
        if person["name"]==name:
            person_dict=person
    if request.method=='GET':
        edit_form=f"""
                   <html>
                    <body>
                        <h1><a href='/'>Hannah and her friends</a></h1>
                        <fieldset> 
                            <legend>Update your Information!</legend>
                                <form action='/update/{name}' method='POST'>              
                                    <p><b>Name</b> : <input type='text' name='name' value={person_dict["name"]}></p>
                                    <p><b>Password</b> : <input type='password' name='pw'> (Only 4 numbers are allowed!)</p>
                                    </hr> 
                                    <p><b>Age</b>  : <input type='text' value='{person_dict["age"]}' name='age'></p>
                                    <p><b>Gender</b>:      
                                             <input type='radio' name='gender' value='Male'>Male 
                                             <input type='radio' name='gender' value='Female'>Female<p>
                                    <input type='submit' value='submit'>
                                </form>
                        </fieldset>    
                    </body>
                <html>
        """
    elif request.method =='POST':
            return "a"
    return HttpResponse(edit_form)

@csrf_exempt
def delete(request,name):
    #로그인 화면에서 넘어옴
    global people
    people_list=''
    if request.method=='GET':
        for person in people:
            people_list += f"""<p><input type='checkbox' name='name[]' value={person["name"]}>{person["name"]}</p>"""
        form_script = f"""
                <html>
                    <body>
                        <h1><a href='/'>Hannah and her friends</a></h1>
                        <fieldset> 
                            <legend>Delete</legend>
                            <Choose who you want to delete :(
                            </br>
                            <form action='/delete/delete' method='POST'>
                                {people_list}
                                <input type='submit'>
                            </form>
                        </fieldset>
                    </body>
                <html>
                """
        return HttpResponse(form_script)
    elif request.method =='POST': #뭐가문제냐...
        for person in people:
            #{'name[]':['Hannah','Minji]} 이런식으로 저장됨
            for name in request.POST.getlist('name[]'):
                #POST에 있는 list 가져오기 위해서는 getlist(배열명) 사용해야함
                if person["name"] == name:
                    people.remove(person)
        return redirect('/')
