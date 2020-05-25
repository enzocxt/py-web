from utils import (
    log,
    template,
)
from models.user import User
from models.weibo import Weibo
from . import (
    random_str,
    redirect,
    response_with_headers,
    http_response,
)
from .routes_index import current_user


def index(request):
    """
    weibo 首页的路由函数
    """
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    user = User.find_by(username=uname)
    if user is None:
        return redirect('/login')
    weibos = Weibo.find_all(user_id=user.id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def edit(request):
    """
    weibo edit 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    # 权限
    if t.user_id != u.id:
        return redirect('/login')
    # if todo_id < 1:
    #     return error(404)
    # 替换模板文件中的标记字符串
    body = template('todo_edit.html', todo=t)
    return http_response(body)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        w = Weibo(form, u.id)
        w.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo')


def update(request):
    """
    用于更新 todo 的路由函数
    """
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        todo_id = int(request.query.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')


def delete(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


def login_required(route_func):
    def func(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_func(request)
    return func


route_dict = {
    # GET 请求，显示页面
    '/weibo': index,
    '/weibo/new': new,
    '/weibo/edit': edit,
    # POST 请求，处理数据
    '/weibo/add': add,
    '/weibo/update': login_required(update),
    '/weibo/delete': delete,
}
