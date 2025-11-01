import pytest
import flask
from werkzeug.http import parse_set_header
import flask.views

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_methodview_basic_and_inheritance(app, client):
    # 1. MethodView 基础 GET/POST + OPTIONS 自动生成
    class BaseView(flask.views.MethodView):
        def get(self):
            return "OK"

        def post(self):
            return "POSTED"

    class ChildView(BaseView):
        def delete(self):
            return "REMOVED"

    app.add_url_rule("/", view_func=ChildView.as_view("index"))

    # 测试 GET/POST/DELETE/OPTIONS
    rv = client.get("/")
    assert rv.data == b"OK"

    rv = client.post("/")
    assert rv.data == b"POSTED"

    rv = client.delete("/")
    assert rv.data == b"REMOVED"

    meths = parse_set_header(client.open("/", method="OPTIONS").headers["Allow"])
    assert sorted(meths) == ["DELETE", "GET", "HEAD", "OPTIONS", "POST"]


def test_view_decorators_and_dispatch(app, client):
    # 2. View + 装饰器
    def add_x_magic(f):
        def new_func(*args, **kwargs):
            resp = flask.make_response(f(*args, **kwargs))
            resp.headers["X-Magic"] = "super"
            return resp
        return new_func

    class DecoratedView(flask.views.View):
        decorators = [add_x_magic]

        def dispatch_request(self):
            return "Super"

    app.add_url_rule("/decorated", view_func=DecoratedView.as_view("decorated"))
    rv = client.get("/decorated")
    assert rv.data == b"Super"
    assert rv.headers["X-Magic"] == "super"


def test_multiple_methods_inheritance_and_removal(app, client):
    # 3. 多继承 + 移除父类方法
    class GetView(flask.views.MethodView):
        def get(self):
            return "OK"

    class OtherView(flask.views.MethodView):
        def post(self):
            return "POSTED"

    class CustomView(GetView, OtherView):
        methods = ["GET"]  # 移除 POST

    app.add_url_rule("/custom", view_func=CustomView.as_view("custom"))

    # GET 存在
    rv = client.get("/custom")
    assert rv.data == b"OK"

    # POST 被移除
    rv = client.post("/custom")
    assert rv.status_code == 405
