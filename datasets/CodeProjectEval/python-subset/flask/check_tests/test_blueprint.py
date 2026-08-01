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

def test_modular_error_handling(app, client):
    """
    Tests that different blueprints can define their own handlers 
    for the same error code.
    """
    api = flask.Blueprint("api", __name__)
    web = flask.Blueprint("web", __name__)
    admin = flask.Blueprint("admin", __name__)

    @api.errorhandler(500)
    def api_server_error(e):
        return flask.jsonify(error="API Internal Error"), 500

    @web.errorhandler(500)
    def web_server_error(e):
        return "<h1>Website ran into a problem</h1>", 500

    @api.route("/api/crash")
    def api_crash():
        flask.abort(500)

    @web.route("/web/crash")
    def web_crash():
        flask.abort(500)

    @admin.route("/admin/crash")
    def admin_crash():
        flask.abort(500)

    app.register_blueprint(api)
    app.register_blueprint(web)
    app.register_blueprint(admin)

    # Application's own fallback handler
    @app.errorhandler(500)
    def app_server_error(e):
        return "Application Global Error", 500

    # API blueprint should use its own 500 handler
    rv_api = client.get("/api/crash")
    assert rv_api.status_code == 500
    assert rv_api.json == {"error": "API Internal Error"}

    # Web blueprint should use its own 500 handler
    rv_web = client.get("/web/crash")
    assert rv_web.status_code == 500
    assert rv_web.data == b"<h1>Website ran into a problem</h1>"

    # Admin blueprint did not define a 500 handler, 
    # should fall back to the app's handler
    rv_admin = client.get("/admin/crash")
    assert rv_admin.status_code == 500
    assert rv_admin.data == b"Application Global Error"


def test_global_error_handling_from_blueprint(app, client):
    """
    Tests that a blueprint can register a global error handler 
    using app_errorhandler.
    """
    monitoring = flask.Blueprint("monitoring", __name__)

    @monitoring.app_errorhandler(503)
    def service_unavailable_handler(e):
        return "Service temporarily unavailable, please try again later", 503

    @app.route("/health")
    def app_health_check():
        flask.abort(503)  # Simulate service unavailable

    payments_bp = flask.Blueprint("payments_bp", __name__)

    @payments_bp.route("/checkout")
    def bp_checkout():
        flask.abort(503)  # Simulate payment service unavailable

    app.register_blueprint(monitoring)
    app.register_blueprint(payments_bp)

    # Both routes (one on app, one on_bp) should trigger the global 
    # handler registered by the monitoring blueprint
    assert (
        client.get("/health").data
        == b"Service temporarily unavailable, please try again later"
    )
    assert (
        client.get("/checkout").data
        == b"Service temporarily unavailable, please try again later"
    )


def test_blueprint_routing_and_prefix(app, client):
    """
    Tests how a blueprint's url_prefix combines correctly 
    with its route rules.
    """
    # Using /api/v1/ as the prefix
    api_v1 = flask.Blueprint("api_v1", __name__, url_prefix="/api/v1")

    @api_v1.route("/users")
    def get_users():
        return "list of users"

    @api_v1.route("profile")  # Test route without a leading slash
    def get_profile():
        return "user profile"

    app.register_blueprint(api_v1)

    # Check if routes are registered correctly
    assert client.get("/api/v1/users").data == b"list of users"
    assert client.get("/api/v1/profile").data == b"user profile"

    # Check if url_for builds correctly
    with app.test_request_context():
        assert flask.url_for("api_v1.get_users") == "/api/v1/users"
        assert flask.url_for("api_v1.get_profile") == "/api/v1/profile"


def test_blueprint_request_lifecycle(app, client):
    """
    Tests blueprint-specific request hooks: before, after, and teardown.
    """
    bp = flask.Blueprint("bp", __name__)
    events_log = []

    @bp.before_request
    def bp_before():
        events_log.append("bp_before")
        flask.g.user = "test_user"

    @bp.after_request
    def bp_after(response):
        events_log.append("bp_after")
        response.headers["X-Blueprint-Processed"] = "true"
        return response

    @bp.teardown_request
    def bp_teardown(exc):
        events_log.append("bp_teardown")
        # g.user is still available
        assert flask.g.user == "test_user"

    @bp.route("/data")
    def bp_data():
        events_log.append("bp_view")
        assert flask.g.user == "test_user"
        return "view data"

    app.register_blueprint(bp, url_prefix="/bp")

    assert events_log == []
    rv = client.get("/bp/data")
    assert rv.data == b"view data"
    assert rv.headers["X-Blueprint-Processed"] == "true"
    assert events_log == ["bp_before", "bp_view", "bp_after", "bp_teardown"]


def test_blueprint_context_injection(app, client):
    """
    Tests app_context_processor (global) and 
    context_processor (blueprint-local).
    """
    auth_bp = flask.Blueprint("auth_bp", __name__)

    def render_template():
        # Helper function to render a template string
        return flask.render_template_string(
            "Site: {{ site_name }}. User: {% if current_user %}{{ current_user }}{% else %}Guest{% endif %}"
        )

    # Should be available in all requests
    @auth_bp.app_context_processor
    def inject_site_name():
        return {"site_name": "MyGlobalSite"}

    # Should only be available in auth_bp's requests
    @auth_bp.context_processor
    def inject_current_user():
        return {"current_user": "admin_user"}

    # Blueprint route for testing
    @auth_bp.route("/auth/profile")
    def bp_page():
        return render_template()

    # App route for testing
    @app.route("/")
    def app_page():
        return render_template()

    app.register_blueprint(auth_bp)

    # App route should only see the global context
    app_page_data = client.get("/").data
    assert b"Site: MyGlobalSite" in app_page_data
    assert b"User: Guest" in app_page_data

    # Blueprint route should see both global and local contexts
    bp_page_data = client.get("/auth/profile").data
    assert b"Site: MyGlobalSite" in bp_page_data
    assert b"User: admin_user" in bp_page_data


def test_dynamic_url_processors(app, client):
    """
    Tests using url_value_preprocessor and url_defaults 
    to handle dynamic URL parts (e.g., multi-tenancy).
    """
    tenant_bp = flask.Blueprint("tenant_bp", __name__, url_prefix="/<tenant_id>")

    @tenant_bp.url_value_preprocessor
    def pull_tenant_id(endpoint, values):
        # Extract tenant_id from URL and put it in g
        if "tenant_id" in values:
            flask.g.tenant_id = values.pop("tenant_id")

    @tenant_bp.url_defaults
    def add_tenant_id(endpoint, values):
        # Automatically add g.tenant_id in url_for
        if "tenant_id" not in values and hasattr(flask.g, "tenant_id"):
            values["tenant_id"] = flask.g.tenant_id

    @tenant_bp.route("/dashboard")
    def dashboard():
        # .settings should automatically get <tenant_id>
        return flask.url_for(".settings")

    @tenant_bp.route("/settings")
    def settings():
        # .dashboard should automatically get <tenant_id>
        return flask.url_for(".dashboard")

    app.register_blueprint(tenant_bp)

    # Test tenant 'acme'
    assert client.get("/acme/dashboard").data == b"/acme/settings"
    # Test tenant 'globex'
    assert client.get("/globex/settings").data == b"/globex/dashboard"


def test_nested_blueprints_and_error_propagation(app, client):
    """
    Tests blueprint nesting, including URL prefix combination
    and error handler propagation.
    """
    import flask

    # Define geographic blueprints
    region_bp = flask.Blueprint("region", __name__, url_prefix="/<region>")
    country_bp = flask.Blueprint("country", __name__, url_prefix="/<country>")
    city_bp = flask.Blueprint("city", __name__, url_prefix="/<city>")

    # Parent blueprint (region) handles 401
    @region_bp.errorhandler(401)
    def region_unauthorized(e):
        return "Region-level Access Denied", 401

    # Grandchild blueprint (city) handles 404
    @city_bp.errorhandler(404)
    def city_not_found(e):
        return "City Not Found", 404

    # region routes
    @region_bp.route("/status")
    def region_status(region):
        return "Region OK"

    @region_bp.route("/auth_fail")
    def region_fail(region):
        flask.abort(401)

    # country routes (must accept region and country)
    @country_bp.route("/status")
    def country_status(region, country):
        return "Country OK"

    @country_bp.route("/auth_fail")
    def country_fail(region, country):
        flask.abort(401)  # handled by region_bp

    @country_bp.route("/missing")
    def country_missing(region, country):
        flask.abort(404)  # handled by app

    # city routes (must accept region, country, city)
    @city_bp.route("/status")
    def city_status(region, country, city):
        return "City OK"

    @city_bp.route("/missing")
    def city_missing(region, country, city):
        flask.abort(404)  # handled by city_bp

    # Register nesting
    country_bp.register_blueprint(city_bp)
    region_bp.register_blueprint(country_bp)
    app.register_blueprint(region_bp)

    # App-level 404
    @app.errorhandler(404)
    def app_not_found(e):
        return "App-level Not Found", 404

    # Test route combination
    assert client.get("/emea/status").data == b"Region OK"
    assert client.get("/emea/de/status").data == b"Country OK"
    assert client.get("/emea/de/berlin/status").data == b"City OK"

    # Test error propagation
    # region 401 (handled by region_bp)
    assert client.get("/emea/auth_fail").data == b"Region-level Access Denied"
    # country 401 (bubbles up to region_bp)
    assert client.get("/emea/de/auth_fail").data == b"Region-level Access Denied"
    # city 404 (handled by city_bp)
    assert client.get("/emea/de/berlin/missing").data == b"City Not Found"
    # country 404 (bubbles up to app)
    assert client.get("/emea/de/missing").data == b"App-level Not Found"



def test_blueprint_jinja_filters(app, client):
    """
    Tests a blueprint registering an app-global Jinja2 filter.
    """
    admin_bp = flask.Blueprint("admin_bp", __name__)

    @admin_bp.app_template_filter("format_currency")
    def _format_currency(value):
        return f"${value:,.2f}"

    @admin_bp.app_template_filter()
    def to_uppercase(s):
        return s.upper()

    # Before registration, filter does not exist
    assert "format_currency" not in app.jinja_env.filters
    assert "to_uppercase" not in app.jinja_env.filters

    app.register_blueprint(admin_bp)

    # After registration, filter should be globally available
    assert "format_currency" in app.jinja_env.filters
    assert "to_uppercase" in app.jinja_env.filters

    @app.route("/report")
    def report():
        # Template string tests both filters
        template = (
            "Total: {{ 12345.6 | format_currency }}. Title: {{ 'hello' | to_uppercase }}"
        )
        return flask.render_template_string(template)

    rv = client.get("/report")
    assert rv.data == b"Total: $12,345.60. Title: HELLO"