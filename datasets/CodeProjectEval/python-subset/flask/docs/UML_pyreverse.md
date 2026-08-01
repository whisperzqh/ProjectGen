## UML Class Diagram
```mermaid
classDiagram
  class Flask {
    cli
    debug
    default_config : ImmutableDict
    request_class : type[Request]
    response_class : type[Response]
    session_interface
    app_context() AppContext
    async_to_sync(func: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]]) t.Callable[..., t.Any]
    create_jinja_environment() Environment
    create_url_adapter(request: Request | None) MapAdapter | None
    dispatch_request() ft.ResponseReturnValue
    do_teardown_appcontext(exc: BaseException | None) None
    do_teardown_request(exc: BaseException | None) None
    ensure_sync(func: t.Callable[..., t.Any]) t.Callable[..., t.Any]
    finalize_request(rv: ft.ResponseReturnValue | HTTPException, from_error_handler: bool) Response
    full_dispatch_request() Response
    get_send_file_max_age(filename: str | None) int | None
    handle_exception(e: Exception) Response
    handle_http_exception(e: HTTPException) HTTPException | ft.ResponseReturnValue
    handle_user_exception(e: Exception) HTTPException | ft.ResponseReturnValue
    log_exception(exc_info: tuple[type, BaseException, TracebackType] | tuple[None, None, None]) None
    make_default_options_response() Response
    make_response(rv: ft.ResponseReturnValue) Response
    make_shell_context() dict[str, t.Any]
    open_instance_resource(resource: str, mode: str, encoding: str | None) t.IO[t.AnyStr]
    open_resource(resource: str, mode: str, encoding: str | None) t.IO[t.AnyStr]
    preprocess_request() ft.ResponseReturnValue | None
    process_response(response: Response) Response
    raise_routing_exception(request: Request) t.NoReturn
    request_context(environ: WSGIEnvironment) AppContext
    run(host: str | None, port: int | None, debug: bool | None, load_dotenv: bool) None
    send_static_file(filename: str) Response
    test_cli_runner() FlaskCliRunner
    test_client(use_cookies: bool) FlaskClient
    test_request_context() AppContext
    update_template_context(context: dict[str, t.Any]) None
    url_for() str
    wsgi_app(environ: WSGIEnvironment, start_response: StartResponse) cabc.Iterable[bytes]
  }
  class Blueprint {
    cli
    get_send_file_max_age(filename: str | None) int | None
    open_resource(resource: str, mode: str, encoding: str | None) t.IO[t.AnyStr]
    send_static_file(filename: str) Response
  }
  class AppGroup {
    name : str
    command() t.Callable[[t.Callable[..., t.Any]], click.Command]
    group() t.Callable[[t.Callable[..., t.Any]], click.Group]
  }
  class CertParamType {
    name : str
    path_type : Path
    convert(value: t.Any, param: click.Parameter | None, ctx: click.Context | None) t.Any
  }
  class FlaskGroup {
    create_app : t.Callable[..., Flask] | None
    load_dotenv : bool
    set_debug_flag : bool
    get_command(ctx: click.Context, name: str) click.Command | None
    list_commands(ctx: click.Context) list[str]
    make_context(info_name: str | None, args: list[str], parent: click.Context | None) click.Context
    parse_args(ctx: click.Context, args: list[str]) list[str]
  }
  class NoAppException {
  }
  class ScriptInfo {
    app_import_path : str | None
    create_app : t.Callable[..., Flask] | None
    data : dict[t.Any, t.Any]
    load_dotenv_defaults : bool
    set_debug_flag : bool
    load_app() Flask
  }
  class SeparatedPathType {
    convert(value: t.Any, param: click.Parameter | None, ctx: click.Context | None) t.Any
  }
  class Config {
    root_path : str | os.PathLike[str]
    from_envvar(variable_name: str, silent: bool) bool
    from_file(filename: str | os.PathLike[str], load: t.Callable[[t.IO[t.Any]], t.Mapping[str, t.Any]], silent: bool, text: bool) bool
    from_mapping(mapping: t.Mapping[str, t.Any] | None) bool
    from_object(obj: object | str) None
    from_prefixed_env(prefix: str) bool
    from_pyfile(filename: str | os.PathLike[str], silent: bool) bool
    get_namespace(namespace: str, lowercase: bool, trim_namespace: bool) dict[str, t.Any]
  }
  class ConfigAttribute {
    get_converter : t.Callable[[t.Any], T] | None
  }
  class AppContext {
    app
    g
    has_request
    request
    session
    url_adapter : MapAdapter | None
    copy() te.Self
    from_environ() te.Self
    match_request() None
    pop(exc: BaseException | None) None
    push() None
  }
  class _AppCtxGlobals {
    get(name: str, default: t.Any | None) t.Any
    pop(name: str, default: t.Any) t.Any
    setdefault(name: str, default: t.Any) t.Any
  }
  class DebugFilesKeyError {
    msg : str
  }
  class FormDataRoutingRedirect {
  }
  class UnexpectedUnicodeError {
  }
  class newcls {
  }
  class AppContextProxy {
  }
  class FlaskProxy {
  }
  class ProxyMixin {
  }
  class RequestProxy {
  }
  class SessionMixinProxy {
  }
  class _AppCtxGlobalsProxy {
  }
  class DefaultJSONProvider {
    compact : bool | None
    default : t.Callable[[t.Any], t.Any]
    ensure_ascii : bool
    mimetype : str
    sort_keys : bool
    dumps(obj: t.Any) str
    loads(s: str | bytes) t.Any
    response() Response
  }
  class JSONProvider {
    dump(obj: t.Any, fp: t.IO[str]) None
    dumps(obj: t.Any)* str
    load(fp: t.IO[t.AnyStr]) t.Any
    loads(s: str | bytes)* t.Any
    response() Response
  }
  class JSONTag {
    key : str
    serializer
    check(value: t.Any)* bool
    tag(value: t.Any) dict[str, t.Any]
    to_json(value: t.Any)* t.Any
    to_python(value: t.Any)* t.Any
  }
  class PassDict {
    tag
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
  }
  class PassList {
    tag
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
  }
  class TagBytes {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TagDateTime {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TagDict {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TagMarkup {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TagTuple {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TagUUID {
    key : str
    check(value: t.Any) bool
    to_json(value: t.Any) t.Any
    to_python(value: t.Any) t.Any
  }
  class TaggedJSONSerializer {
    default_tags : list
    order : list[JSONTag]
    tags : dict[str, JSONTag]
    dumps(value: t.Any) str
    loads(value: str) t.Any
    register(tag_class: type[JSONTag], force: bool, index: int | None) None
    tag(value: t.Any) t.Any
    untag(value: dict[str, t.Any]) t.Any
  }
  class NullSession {
    clear
    pop
    popitem
    setdefault
    update
  }
  class SecureCookieSession {
    accessed : bool
    modified : bool
    get(key: str, default: t.Any) t.Any
    setdefault(key: str, default: t.Any) t.Any
  }
  class SecureCookieSessionInterface {
    digest_method : staticmethod
    key_derivation : str
    salt : str
    serializer
    session_class
    get_signing_serializer(app: Flask) URLSafeTimedSerializer | None
    open_session(app: Flask, request: Request) SecureCookieSession | None
    save_session(app: Flask, session: SessionMixin, response: Response) None
  }
  class SessionInterface {
    null_session_class
    pickle_based : bool
    get_cookie_domain(app: Flask) str | None
    get_cookie_httponly(app: Flask) bool
    get_cookie_name(app: Flask) str
    get_cookie_partitioned(app: Flask) bool
    get_cookie_path(app: Flask) str
    get_cookie_samesite(app: Flask) str | None
    get_cookie_secure(app: Flask) bool
    get_expiration_time(app: Flask, session: SessionMixin) datetime | None
    is_null_session(obj: object) bool
    make_null_session(app: Flask) NullSession
    open_session(app: Flask, request: Request)* SessionMixin | None
    save_session(app: Flask, session: SessionMixin, response: Response)* None
    should_set_cookie(app: Flask, session: SessionMixin) bool
  }
  class SessionMixin {
    accessed : bool
    modified : bool
    new : bool
    permanent
  }
  class DispatchingJinjaLoader {
    app : App
    get_source(environment: BaseEnvironment, template: str) tuple[str, str | None, t.Callable[[], bool] | None]
    list_templates() list[str]
  }
  class Environment {
    app : App
  }
  class EnvironBuilder {
    app
    json_dumps(obj: t.Any) str
  }
  class FlaskCliRunner {
    app
    invoke(cli: t.Any, args: t.Any) Result
  }
  class FlaskClient {
    application
    environ_base : dict
    preserve_context : bool
    open() TestResponse
    session_transaction() t.Iterator[SessionMixin]
  }
  class MethodView {
    dispatch_request() ft.ResponseReturnValue
  }
  class View {
    decorators : t.ClassVar[list[t.Callable[..., t.Any]]]
    init_every_request : t.ClassVar[bool]
    methods : Optional[t.ClassVar[t.Collection[str] | None]]
    provide_automatic_options : Optional[t.ClassVar[bool | None]]
    as_view(name: str) ft.RouteCallable
    dispatch_request()* ft.ResponseReturnValue
  }
  class Request {
    blueprint
    blueprints
    endpoint
    json_module
    max_content_length
    max_form_memory_size
    max_form_parts
    routing_exception : HTTPException | None
    url_rule : Rule | None
    view_args : dict[str, t.Any] | None
    on_json_loading_failed(e: ValueError | None) t.Any
  }
  class Response {
    autocorrect_location_header : bool
    default_mimetype : str | None
    json_module
    max_cookie_size
    status
    status_code
  }
  FlaskGroup --|> AppGroup
  AppContextProxy --|> AppContext
  AppContextProxy --|> ProxyMixin
  FlaskProxy --|> Flask
  FlaskProxy --|> ProxyMixin
  RequestProxy --|> ProxyMixin
  RequestProxy --|> Request
  SessionMixinProxy --|> ProxyMixin
  SessionMixinProxy --|> SessionMixin
  _AppCtxGlobalsProxy --|> _AppCtxGlobals
  _AppCtxGlobalsProxy --|> ProxyMixin
  DefaultJSONProvider --|> JSONProvider
  PassDict --|> JSONTag
  PassList --|> JSONTag
  TagBytes --|> JSONTag
  TagDateTime --|> JSONTag
  TagDict --|> JSONTag
  TagMarkup --|> JSONTag
  TagTuple --|> JSONTag
  TagUUID --|> JSONTag
  NullSession --|> SecureCookieSession
  SecureCookieSession --|> SessionMixin
  SecureCookieSessionInterface --|> SessionInterface
  MethodView --|> View
  Flask --* FlaskClient : application
  AppGroup --* Flask : cli
  AppGroup --* Blueprint : cli
  _AppCtxGlobals --* AppContext : g
  TaggedJSONSerializer --* SecureCookieSessionInterface : serializer
  NullSession --* SessionInterface : null_session_class
  SecureCookieSession --* SecureCookieSessionInterface : session_class
  SessionInterface --* Flask : session_interface
  Flask --o AppContext : app
  Flask --o EnvironBuilder : app
  Flask --o FlaskCliRunner : app
  TaggedJSONSerializer --o JSONTag : serializer
```

## UML Package Diagram
```mermaid
classDiagram
  class flask {
  }
  class __main__ {
  }
  class app {
  }
  class blueprints {
  }
  class cli {
  }
  class config {
  }
  class ctx {
  }
  class debughelpers {
  }
  class globals {
  }
  class helpers {
  }
  class json {
  }
  class provider {
  }
  class tag {
  }
  class logging {
  }
  class sessions {
  }
  class signals {
  }
  class templating {
  }
  class testing {
  }
  class typing {
  }
  class views {
  }
  class wrappers {
  }
  flask --> app
  flask --> blueprints
  flask --> config
  flask --> ctx
  flask --> globals
  flask --> helpers
  flask --> json
  flask --> signals
  flask --> templating
  flask --> wrappers
  __main__ --> cli
  app --> ctx
  app --> debughelpers
  app --> globals
  app --> helpers
  app --> sessions
  app --> signals
  app --> templating
  app --> testing
  app --> typing
  app --> wrappers
  blueprints --> cli
  blueprints --> globals
  blueprints --> helpers
  blueprints --> typing
  cli --> globals
  cli --> helpers
  cli --> typing
  config --> json
  config --> typing
  ctx --> globals
  ctx --> signals
  ctx --> typing
  debughelpers --> blueprints
  debughelpers --> globals
  debughelpers --> typing
  globals --> typing
  helpers --> globals
  helpers --> signals
  helpers --> typing
  json --> globals
  json --> provider
  logging --> globals
  logging --> typing
  sessions --> tag
  sessions --> typing
  templating --> debughelpers
  templating --> globals
  templating --> helpers
  templating --> signals
  templating --> typing
  testing --> cli
  testing --> sessions
  testing --> typing
  views --> globals
  views --> typing
  wrappers --> debughelpers
  wrappers --> globals
  wrappers --> helpers
  wrappers --> typing
  app ..> typing
  blueprints ..> wrappers
  cli ..> app
  ctx ..> app
  ctx ..> sessions
  ctx ..> wrappers
  debughelpers ..> wrappers
  globals ..> app
  globals ..> ctx
  globals ..> sessions
  globals ..> wrappers
  helpers ..> wrappers
  json ..> wrappers
  sessions ..> app
  sessions ..> wrappers
  templating ..> app
  testing ..> app
```