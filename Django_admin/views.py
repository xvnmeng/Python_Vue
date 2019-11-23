from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
# 导入数据库模型
from Django_admin.models import User, Article
import json
import hashlib
from functools import wraps
# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            # 定向到登录页面
            return redirect('/login/')
    return inner

def login(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method=="POST":
        req = json.loads(request.body)
        username = req["username"]
        # username=request.POST.get('username')
        # password=request.POST.get('password')
        password = req["password"]
        print(username)
        print(password)
        user=User.objects.filter(username=username,password=password)
        # name = user.username
        # print(name)
        # user=User.objects.get(username=username).password
        if user:
            print(222)
            #登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login']='1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            request.session['user_id']=user[0].id
            return redirect('/index/')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request,'index.html')

@check_login
def index(request):
    # students=Students.objects.all()  ## 说明，objects.all()返回的是二维表，即一个列表，里面包含多个元组
    # return render(request,'index.html',{"students_list":students})
    # username1=request.session.get('username')
    user_id1=request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj=User.objects.filter(id=user_id1)
    print(userobj)
    if userobj:
        return render(request,'index.html',{"user":userobj[0]})
    else:
        return render(request,'index.html',{'user','匿名用户'})





# 接口较多，可以通过文件夹分类
# 新增文章
def add_article(request):
    auth_res = user_auth(request)
    if auth_res == "auth_fail":
        return JsonResponse({"status":"BS.401","msg":"user auth failed."})
    else:
        if request.method == 'POST':
            # 格式化参数
            req = json.loads(request.body)
            # print(req)
            print(request)
            # <WSGIRequest: POST '/articles/'>
            # 根据发送的路径，可以去除id，查询指定的数据
            # 获取到字段标志
            key_flag = req.get('title') and req.get('content') and len(req) == 2
            if key_flag:
                title = req["title"]
                content = req['content']
                title_exist = Article.objects.filter(title=title)
                # 标题是否同名
                if len(title_exist) != 0:
                    return JsonResponse({"status":"BS.400","msg":"title aleady exist,fail to publish."})
                # 插入数据
                add_art = Article(title=title, content=content,status='alive')
                add_art.save()
                return JsonResponse({"status":"BS.200","msg":"publish article sucess."})
            else:
                return  JsonResponse({"status":"BS.400","message":"please check param."})
        #查询所有文章和状态
        if request.method == "GET":
            articles = {}
            query_art = Article.objects.all()
            for title in query_art:
                articles[title.title] = title.status
            return JsonResponse({"status":"BS.200","all_titles":articles,"msg":"query articles sucess."})

# 修改文章
def modify_article(request, art_id):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            art = Article.objects.get(id=art_id)
            key_flag = req.get("title") and req.get("content") and len(req)==2
            if key_flag:
                title = req['title']
                content = req['content']
                # 要修改的标题是否已经存在
                title_exist = Article.objects.filter(title=title)
                if len(title_exist) > 1:
                    return JsonResponse({"status":"BS.400","msg":"title aleady exist."})
                # 更新数据,从数据库取出原有的数据，整体更新回去，不会导致某些字段你为空失败
                old_art = Article.objects.get(id=art_id)
                old_art.title = title
                old_art.content = content
                old_art.save()
                return JsonResponse({"status":"BS.200","msg":"modify article sucess."})
        except Article.DoesNotExist:
            return  JsonResponse({"status":"BS.300","msg":"article is not exists,fail to modify."})
    #删除文章
    if request.method == "DELETE":
        try:
            art = Article.objects.get(id=art_id)
            art_id = art.id
            art.delete()
            return JsonResponse({"status":"BS.200","msg":"delete article sucess."})
        except Article.DoesNotExist:
            return JsonResponse({"status":"BS.300","msg":"article is not exists,fail to delete."})

# 鉴权接口 获取token
def get_token(request):
    req = json.loads(request.body)
    username = req["username"]
    password = req["password"]
    if request.method == "POST":
        try:
            tmp_password =User.objects.get(username=username).password
            if password == tmp_password:
                md5 = hashlib.md5()
                #把密码变成一个长度固定的字符串
                md5.update(password.encode("utf-8"))
                return JsonResponse({"status":"BS.201","X-Token":md5.hexdigest()})
            else:
                return JsonResponse({"status":"BS.401","msg":"username or password may wrong."})
        except User.DoesNotExist:
            return JsonResponse({"status":"BS.500","msg":"username is not exist."})

# 用户认证
#认证动作
def user_auth(request):
    token = request.META.get("HTTP_X_TOKEN",b'')
    print (token)
    if token:
        #暂时先写上auth接口返回的数据
        if token=="0a6db4e59c7fff2b2b94a297e2e5632e":
            return "auth_sucess"
        else:
            return "auth_fail"
    else:
        return  "auth_fail"
