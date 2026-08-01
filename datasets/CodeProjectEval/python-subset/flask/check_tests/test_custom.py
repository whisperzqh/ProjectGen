import pytest
import flask
from werkzeug.http import parse_cache_control_header
from jinja2 import TemplateNotFound

import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600

    # 可选：注册测试模板和蓝图
    app.jinja_env.loader.mapping = {
        "template_filter.html": "{{ value|super_reverse }}",
        "template_test.html": "{% if value is boolean %}Success!{% endif %}",
    }

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_blueprint_specific_error_handling_new(app, client):
    alpha = flask.Blueprint("alpha", __name__)
    beta = flask.Blueprint("beta", __name__)
    gamma = flask.Blueprint("gamma", __name__)

    @alpha.errorhandler(404)
    def alpha_not_found(e):
        return "alpha missing", 404

    @alpha.route("/alpha-missing")
    def alpha_route():
        flask.abort(404)

    @beta.errorhandler(404)
    def beta_not_found(e):
        return "beta missing", 404

    @beta.route("/beta-missing")
    def beta_route():
        flask.abort(404)

    @gamma.route("/gamma-test")
    def gamma_route():
        flask.abort(404)

    app.register_blueprint(alpha)
    app.register_blueprint(beta)
    app.register_blueprint(gamma)

    @app.errorhandler(404)
    def app_not_found(e):
        return "app missing", 404

    assert client.get("/alpha-missing").data == b"alpha missing"
    assert client.get("/beta-missing").data == b"beta missing"
    assert client.get("/gamma-test").data == b"app missing"


def test_blueprint_specific_user_error_handling_new(app, client):
    class DecoratorError(Exception):
        pass

    class FunctionError(Exception):
        pass

    bp = flask.Blueprint("bp", __name__)

    @bp.errorhandler(DecoratorError)
    def handle_decorator_error(e):
        return "fail1"

    def handle_function_error(e):
        return "fail2"

    bp.register_error_handler(FunctionError, handle_function_error)

    @bp.route("/deco")
    def deco_route():
        raise DecoratorError()

    @bp.route("/func")
    def func_route():
        raise FunctionError()

    app.register_blueprint(bp)

    assert client.get("/deco").data == b"fail1"
    assert client.get("/func").data == b"fail2"


def test_blueprint_url_defaults_new(app, client):
    bp = flask.Blueprint("bp", __name__)

    @bp.route("/item", defaults={"val": 7})
    def item_route(key, val):
        return f"{key}/{val}"

    @bp.route("/thing")
    def thing_route(key):
        return str(key)

    app.register_blueprint(bp, url_prefix="/x", url_defaults={"key": 99})
    app.register_blueprint(bp, name="bp2", url_prefix="/y", url_defaults={"key": 17})

    assert client.get("/x/item").data == b"99/7"
    assert client.get("/y/item").data == b"17/7"
    assert client.get("/x/thing").data == b"99"
    assert client.get("/y/thing").data == b"17"


def test_blueprint_url_processors_new(app, client):
    bp = flask.Blueprint("frontend", __name__, url_prefix="/<region>")

    @bp.url_defaults
    def add_region(endpoint, values):
        values.setdefault("region", flask.g.region)

    @bp.url_value_preprocessor
    def pull_region(endpoint, values):
        flask.g.region = values.pop("region")

    @bp.route("/")
    def home():
        return flask.url_for(".info")

    @bp.route("/info")
    def info():
        return flask.url_for(".home")

    app.register_blueprint(bp)

    assert client.get("/us/").data == b"/us/info"
    assert client.get("/us/info").data == b"/us/"

'''
def test_default_static_max_age_new(app):
    class CustomBlueprint(flask.Blueprint):
        def get_send_file_max_age(self, filename):
            return 200

    bp = CustomBlueprint("custom", __name__, static_folder="static")
    app.register_blueprint(bp)

    max_age_default = app.config["SEND_FILE_MAX_AGE_DEFAULT"]
    try:
        unexpected_max_age = 3600 if max_age_default != 3600 else 7200
        app.config["SEND_FILE_MAX_AGE_DEFAULT"] = unexpected_max_age
        with app.test_request_context():
            rv = bp.send_static_file("index.html")
            cc = parse_cache_control_header(rv.headers["Cache-Control"])
            assert cc.max_age == 200
            rv.close()
    finally:
        app.config["SEND_FILE_MAX_AGE_DEFAULT"] = max_age_default
'''

def test_template_filter_new(app):
    bp = flask.Blueprint("bp", __name__)

    @bp.app_template_filter()
    def double_string(s):
        return s * 2

    app.register_blueprint(bp, url_prefix="/py")
    with app.app_context():
        assert app.jinja_env.filters["double_string"]("ab") == "abab"


def test_template_test_new(app, client):
    bp = flask.Blueprint("bp", __name__)

    @bp.app_template_test()
    def is_list(v):
        return isinstance(v, list)

    app.register_blueprint(bp, url_prefix="/py")

    @app.route("/")
    def index():
        return flask.render_template_string("{% if value is is_list %}Yes{% else %}No{% endif %}", value=[1,2,3])

    rv = client.get("/")
    assert rv.data == b"Yes"


def test_context_processing_new(app, client):
    bp = flask.Blueprint("bp", __name__)

    @bp.app_context_processor
    def global_context():
        return {"global_val": 100}

    @bp.context_processor
    def local_context():
        return {"local_val": 200}

    @bp.route("/test")
    def test_route():
        return flask.render_template_string("{{ global_val }},{{ local_val }}")

    app.register_blueprint(bp)
    rv = client.get("/test")
    assert rv.data == b"100,200"


def test_request_processing_new(app, client):
    bp = flask.Blueprint("bp", __name__)
    events = []

    @bp.before_request
    def before():
        events.append("before")

    @bp.after_request
    def after(response):
        response.data += b"|done"
        events.append("after")
        return response

    @bp.teardown_request
    def teardown(exc):
        events.append("teardown")

    @bp.route("/r")
    def r():
        return "go"

    app.register_blueprint(bp)
    rv = client.get("/r")
    assert rv.data == b"go|done"
    assert events == ["before", "after", "teardown"]


def test_nested_blueprint_new(app, client):
    parent = flask.Blueprint("parent", __name__)
    child = flask.Blueprint("child", __name__)
    grandchild = flask.Blueprint("grandchild", __name__)

    @parent.errorhandler(401)
    def forbidden(e):
        return "Parent denied", 401

    @parent.route("/")
    def parent_index():
        return "Parent ok"

    @child.route("/")
    def child_index():
        return "Child ok"

    @grandchild.errorhandler(401)
    def grandchild_forbidden(e):
        return "Grandchild denied", 401

    @grandchild.route("/")
    def grandchild_index():
        return "Grandchild ok"

    child.register_blueprint(grandchild, url_prefix="/gc")
    parent.register_blueprint(child, url_prefix="/ch")
    app.register_blueprint(parent, url_prefix="/pr")

    assert client.get("/pr/").data == b"Parent ok"
    assert client.get("/pr/ch/").data == b"Child ok"
    assert client.get("/pr/ch/gc/").data == b"Grandchild ok"

def test_provide_automatic_options_attr_updated():
    """
    Tests disabling automatic OPTIONS handling via a function attribute on the
    view function.
    """
    # Test case 1: automatic options are disabled
    app = flask.Flask(__name__)

    def no_options_view():
        return "This view has no automatic OPTIONS."

    no_options_view.provide_automatic_options = False
    app.route("/no-opts")(no_options_view)
    rv = app.test_client().open("/no-opts", method="OPTIONS")
    assert rv.status_code == 405  # Method Not Allowed

    # Test case 2: explicit OPTIONS handler with automatic options enabled
    app = flask.Flask(__name__)

    def manual_options_view():
        return "This is a manual OPTIONS response."

    # This is slightly redundant but confirms the attribute is respected
    # even when OPTIONS is manually listed.
    manual_options_view.provide_automatic_options = True
    app.route("/manual-opts", methods=["OPTIONS"])(manual_options_view)
    rv = app.test_client().open("/manual-opts", method="OPTIONS")
    assert rv.status_code == 200
    assert sorted(rv.allow) == ["OPTIONS"]


def test_provide_automatic_options_kwarg_updated(app, client):
    """
    Tests disabling automatic OPTIONS handling via a keyword argument in
    add_url_rule.
    """
    def first_view():
        return f"Request Method: {flask.request.method}"

    def second_view():
        return f"Request Method: {flask.request.method}"

    app.add_url_rule("/no-auto-options", view_func=first_view, provide_automatic_options=False)
    app.add_url_rule(
        "/more-no-auto",
        view_func=second_view,
        methods=["GET", "POST"],
        provide_automatic_options=False,
    )
    assert client.get("/no-auto-options").data == b"Request Method: GET"

    rv = client.post("/no-auto-options")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD"]

    rv = client.open("/no-auto-options", method="OPTIONS")
    assert rv.status_code == 405

    rv = client.head("/no-auto-options")
    assert rv.status_code == 200
    assert not rv.data  # HEAD responses have no body

    assert client.post("/more-no-auto").data == b"Request Method: POST"
    assert client.get("/more-no-auto").data == b"Request Method: GET"

    rv = client.delete("/more-no-auto")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "POST"]

    rv = client.open("/more-no-auto", method="OPTIONS")
    assert rv.status_code == 405


def test_request_dispatching_updated(app, client):
    """
    A general test for basic request dispatching and method handling.
    """
    @app.route("/home")
    def home_view():
        return f"Home: {flask.request.method}"

    @app.route("/data", methods=["GET", "PUT"])
    def data_view():
        return f"Data: {flask.request.method}"

    assert client.get("/home").data == b"Home: GET"
    rv = client.post("/home")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS"]

    rv = client.head("/home")
    assert rv.status_code == 200
    assert not rv.data

    assert client.put("/data").data == b"Data: PUT"
    assert client.get("/data").data == b"Data: GET"

    rv = client.delete("/data")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS", "PUT"]


def test_disallow_string_for_allowed_methods_updated(app):
    """
    Ensures that providing a space-separated string for the 'methods'
    argument is not allowed; it must be a list or tuple.
    """
    with pytest.raises(TypeError):
        app.add_url_rule("/invalid", methods="GET PUT", endpoint="invalid_test")


def test_url_mapping_updated(app, client):
    """
    Tests url mapping with add_url_rule and ensures non-uppercase methods
    do not trigger automatic OPTIONS handling.
    """
    config_uuid = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

    def primary_view():
        return flask.request.method

    def secondary_view():
        return flask.request.method

    def custom_options_view():
        return config_uuid

    app.add_url_rule("/primary", "primary_endpoint", primary_view)
    app.add_url_rule("/secondary", "secondary_endpoint", secondary_view, methods=["GET", "POST"])
    # Test that 'options' in lowercase does not create an automatic OPTIONS rule.
    app.add_url_rule("/config", "config_endpoint", custom_options_view, methods=["options"])

    assert client.get("/primary").data == b"GET"
    rv = client.post("/primary")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS"]

    rv = client.head("/primary")
    assert rv.status_code == 200
    assert not rv.data

    assert client.post("/secondary").data == b"POST"
    assert client.get("/secondary").data == b"GET"
    rv = client.delete("/secondary")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS", "POST"]

    # This should hit the custom_options_view because the method is 'options'
    rv = client.open("/config", method="OPTIONS")
    assert rv.status_code == 200
    assert config_uuid in rv.data.decode("utf-8")

