# Architecture Design

Below is a text-based representation of the file tree.

### 目录结构

```text
.
├── flask
│   ├── app.py
│   ├── blueprints.py
│   ├── cli.py
│   ├── config.py
│   ├── ctx.py
│   ├── debughelpers.py
│   ├── globals.py
│   ├── helpers.py
│   ├── __init__.py
│   ├── json
│   │   ├── __init__.py
│   │   ├── provider.py
│   │   └── tag.py
│   ├── logging.py
│   ├── __main__.py
│   ├── py.typed
│   ├── sansio
│   │   ├── app.py
│   │   ├── blueprints.py
│   │   ├── README.md
│   │   └── scaffold.py
│   ├── sessions.py
│   ├── signals.py
│   ├── templating.py
│   ├── testing.py
│   ├── typing.py
│   ├── views.py
│   └── wrappers.py
```

`__init__.py` : This module serves as the public API for Flask, exposing core classes, functions, and objects for easy access. It re-exports important components from submodules so users can import directly from `flask`.

`__main__.py` :

- `main()`: Entry point for the package when executed as a script. Imports and runs the CLI `main` function.

`app.py` :

- `_make_timedelta(value: timedelta | int | None)`: Converts an integer or `None` value into a `timedelta` object (interpreting the integer as seconds), or returns a `timedelta` value unchanged.

- `__init__(self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = 'static', static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | os.PathLike[str] | None = 'templates', instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None)`: Initializes the Flask application, setting up its properties, inheriting from `App`, and configuring the static files route if `static_folder` is set.

- `get_send_file_max_age(self, filename: str | None)`: Used by :func:`send_file` to determine the ``max_age`` cache value for a given file path if it wasn't passed. By default, this returns :data:`SEND_FILE_MAX_AGE_DEFAULT` from the configuration of :data:`~flask.current_app`. This defaults to ``None``, which tells the browser to use conditional requests instead of a timed cache, which is usually preferable.

- `send_static_file(self, filename: str)`: The view function used to serve files from :attr:`static_folder`. A route is automatically registered for this view at :attr:`static_url_path` if :attr:`static_folder` is set.

- `open_resource(self, resource: str, mode: str = 'rb', encoding: str | None = None)`: Open a resource file relative to :attr:`root_path` for reading.

- `open_instance_resource(self, resource: str, mode: str = 'rb', encoding: str | None = 'utf-8')`: Open a resource file relative to the application's instance folder :attr:`instance_path`. Unlike :meth:`open_resource`, files in the instance folder can be opened for writing.

- `create_jinja_environment(self)`: Create the Jinja environment based on :attr:`jinja_options` and the various Jinja-related methods of the app. Changing :attr:`jinja_options` after this will have no effect. Also adds Flask-related globals and filters to the environment.

- `create_url_adapter(self, request: Request | None)`: Creates a URL adapter for the given request. The URL adapter is created at a point where the request context is not yet set up so the request is passed explicitly.

- `raise_routing_exception(self, request: Request)`: Intercept routing exceptions and possibly do something else. In debug mode, intercept a routing redirect and replace it with an error if the body will be discarded.

- `update_template_context(self, context: dict[str, t.Any])`: Update the template context with some commonly used variables. This injects request, session, config and g into the template context as well as everything template context processors want to inject. Note that the as of Flask 0.6, the original values in the context will not be overridden if a context processor decides to return a value with the same key.

- `make_shell_context(self)`: Returns the shell context for an interactive shell for this application. This runs all the registered shell context processors.

- `run(self, host: str | None = None, port: int | None = None, debug: bool | None = None, load_dotenv: bool = True, **options: t.Any)`: Runs the application on a local development server.

- `test_client(self, use_cookies: bool = True, **kwargs: t.Any)`: Creates a test client for this application.

- `test_cli_runner(self, **kwargs: t.Any)`: Create a CLI runner for testing CLI commands.

- `handle_http_exception(self, e: HTTPException)`: Handles an HTTP exception. By default this will invoke the registered error handlers and fall back to returning the exception as response.

- `handle_user_exception(self, e: Exception)`: This method is called whenever an exception occurs that should be handled. A special case is :class:`~werkzeug.exceptions.HTTPException` which is forwarded to the :meth:`handle_http_exception` method. This function will either return a response value or reraise the exception with the same traceback.

- `handle_exception(self, e: Exception)`: Handle an exception that did not have an error handler associated with it, or that was raised from an error handler. This always causes a 500 ``InternalServerError``.

- `log_exception(self, exc_info: (tuple[type, BaseException, TracebackType] | tuple[None, None, None]))`: Logs an exception. This is called by :meth:`handle_exception` if debugging is disabled and right before the handler is called. The default implementation logs the exception as error on the :attr:`logger`.

- `dispatch_request(self)`: Does the request dispatching. Matches the URL and returns the return value of the view or error handler. This does not have to be a response object. In order to convert the return value to a proper response object, call :func:`make_response`.

- `full_dispatch_request(self)`: Dispatches the request and on top of that performs request pre and postprocessing as well as HTTP exception catching and error handling.

- `finalize_request(self, rv: ft.ResponseReturnValue | HTTPException, from_error_handler: bool = False)`: Given the return value from a view function this finalizes the request by converting it into a response and invoking the postprocessing functions. This is invoked for both normal request dispatching as well as error handlers.

- `make_default_options_response(self)`: This method is called to create the default ``OPTIONS`` response. This can be changed through subclassing to change the default behavior of ``OPTIONS`` responses.

- `ensure_sync(self, func: t.Callable[..., t.Any])`: Ensure that the function is synchronous for WSGI workers. Plain ``def`` functions are returned as-is. ``async def`` functions are wrapped to run and wait for the response.

- `async_to_sync(self, func: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]])`: Return a sync function that will run the coroutine function.

- `url_for(self, /, endpoint: str, *, _anchor: str | None = None, _method: str | None = None, _scheme: str | None = None, _external: bool | None = None, **values: t.Any)`: Generate a URL to the given endpoint with the given values.

- `make_response(self, rv: ft.ResponseReturnValue)`: Convert the return value from a view function to an instance of :attr:`response_class`.

- `preprocess_request(self)`: Called before the request is dispatched. Calls :attr:`url_value_preprocessors` registered with the app and the current blueprint (if any). Then calls :attr:`before_request_funcs` registered with the app and the blueprint.

- `process_response(self, response: Response)`: Can be overridden in order to modify the response object before it's sent to the WSGI server. By default this will call all the :meth:`after_request` decorated functions.

- `do_teardown_request(self, exc: BaseException | None = None)`: Called after the request is dispatched and the response is finalized, right before the request context is popped. Called by :meth:`.AppContext.pop`.

- `do_teardown_appcontext(self, exc: BaseException | None = None)`: Called right before the application context is popped. Called by :meth:`.AppContext.pop`.

- `app_context(self)`: Create an :class:`.AppContext`. When the context is pushed, :data:`.current_app` and :data:`.g` become available.

- `request_context(self, environ: WSGIEnvironment)`: Create an :class:`.AppContext` with request information representing the given WSGI environment. A context is automatically pushed when handling each request. When the context is pushed, :data:`.request`, :data:`.session`, :data:`g:, and :data:`.current_app` become available.

- `test_request_context(self, *args: t.Any, **kwargs: t.Any)`: Create an :class:`.AppContext` with request information created from the given arguments. When the context is pushed, :data:`.request`, :data:`.session`, :data:`g:, and :data:`.current_app` become available.

- `wsgi_app(self, environ: WSGIEnvironment, start_response: StartResponse)`: The actual WSGI application. This is not implemented in :meth:`__call__` so that middlewares can be applied without losing a reference to the app object. Instead of doing this:: `app = MyMiddleware(app)` It's a better idea to do this instead:: `app.wsgi_app = MyMiddleware(app.wsgi_app)` Then you still have the original application object around and can continue to call methods on it.

- `__call__(self, environ: WSGIEnvironment, start_response: StartResponse)`: The WSGI server calls the Flask application object as the WSGI application. This calls :meth:`wsgi_app`, which can be wrapped to apply middleware.

`blueprints.py` :

- `Blueprint(name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None, root_path=None, cli_group=_sentinel)`: Extends `SansioBlueprint` to support Flask-style blueprints with static and template folders, URL prefixes, subdomains, and CLI command registration.

  - `get_send_file_max_age(filename)`: Returns the caching max age in seconds for a given static file. Defaults to the app configuration `SEND_FILE_MAX_AGE_DEFAULT`.

  - `send_static_file(filename)`: Serves a file from the blueprint's `static_folder`. Raises a `RuntimeError` if `static_folder` is not set.

  - `open_resource(resource, mode='rb', encoding='utf-8')`: Opens a resource file relative to the blueprint's `root_path`. Supports text or binary reading modes.

`cli.py` :

- `find_best_app(module: ModuleType) -> Flask`: Given a Python module, attempts to locate the most appropriate Flask application instance in it. Checks for common names, single Flask instances, or factory functions. Raises `NoAppException` if no suitable app is found.

- `_called_with_wrong_args(f: t.Callable[..., Flask]) -> bool`: Determines whether a `TypeError` from calling a function is due to incorrect arguments rather than an error raised inside the function itself.

- `find_app_by_string(module: ModuleType, app_name: str) -> Flask`: Locates a Flask application in a module given a string, which may reference a variable or a factory function with optional arguments. Raises `NoAppException` if the app cannot be found.

- `prepare_import(path: str) -> str`: Converts a filesystem path or Python file into a proper Python module import path and ensures the parent directory is on `sys.path`.

- `locate_app(module_name: str, app_name: str | None, raise_if_not_found: bool = True) -> Flask | None`: Imports a module by name and finds a Flask app in it, optionally raising an exception if none is found.

- `get_version(ctx: click.Context, param: click.Parameter, value: t.Any) -> None`: Click callback that prints Python, Flask, and Werkzeug versions, then exits.

- `ScriptInfo`: Helper class for managing Flask applications when using CLI commands. Handles loading the app, setting debug flags, and storing arbitrary data.

  - `load_app() -> Flask`: Loads and returns the Flask application, using either a factory, import path, or default file names. Raises `NoAppException` if no app is found.

- `with_appcontext(f: F) -> F`: Decorator that ensures a Flask application context is active when executing a function. Typically used for CLI command callbacks.
  - `decorator(ctx: click.Context, /, *args: Any, **kwargs: Any) -> Any`:
  The internal function that wraps the original callback to ensure it runs within a Flask application context.

- `AppGroup(click.Group)`: Subclass of `click.Group` that automatically wraps commands in `with_appcontext` unless disabled. Allows nested groups with the same behavior.
  - `command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], click.Command]`:
  Registers a Click command under this group. This method works like `click.Group.command` but adds integration with Flask's application context.
  - `group(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], click.Group]`:
  Registers a sub-group under this Click group. This method works like `click.Group.group` but defaults the group class to `AppGroup`.

- `_set_app(ctx: click.Context, param: click.Option, value: str | None) -> str | None`: Click option callback to set the `ScriptInfo.app_import_path` for the current CLI context.

- `_set_debug(ctx: click.Context, param: click.Option, value: bool) -> bool | None`: Click option callback to set the `FLASK_DEBUG` environment variable based on the provided flag.

- `_env_file_callback(ctx: click.Context, param: click.Option, value: str | None) -> str | None`: Click callback to load environment variables from a `.env` or `.flaskenv` file using `python-dotenv`.

- `FlaskGroup(AppGroup)`: Click group subclass designed for Flask CLI commands. Handles loading the Flask app, environment files, default commands, and plugin commands.

  - `__init__(self, add_default_commands: bool = True, create_app: Callable[..., Flask] | None = None, add_version_option: bool = True, load_dotenv: bool = True, set_debug_flag: bool = True, **extra: Any) -> None`:
  Initializes an instance of a custom Flask `click.Group` subclass (likely `FlaskGroup` or `AppGroup`), which integrates Flask application features with Click commands.

  - `_load_plugin_commands() -> None`: Loads extra CLI commands registered via `flask.commands` entry points.
  
  - `get_command(ctx: click.Context, name: str) -> click.Command | None`: Returns a CLI command by name, including built-in, plugin, and app-provided commands.
  
  - `list_commands(ctx: click.Context) -> list[str]`: Returns a sorted list of command names, including built-in, plugin, and app-provided commands.
  
  - `make_context(info_name: str | None, args: list[str], parent: click.Context | None = None, **extra) -> click.Context`: Prepares the Click context with a `ScriptInfo` object and sets `FLASK_RUN_FROM_CLI`.
  
  - `parse_args(ctx: click.Context, args: list[str]) -> list[str]`: Ensures eager processing of `--env-file` and `--app` options before command dispatch.

- `_path_is_ancestor(path: str, other: str) -> bool`: Checks if `path` is an ancestor directory of `other`.

- `load_dotenv(path: str | os.PathLike[str] | None = None, load_defaults: bool = True) -> bool`: Loads environment variables from a given file or default `.flaskenv` and `.env` files, without overriding existing environment variables. Returns `True` if at least one variable is loaded.

- `show_server_banner(debug: bool, app_import_path: str | None) -> None`: Prints the Flask app startup banner showing the application path and debug status, skipping if the reloader is active.

- `CertParamType(click.ParamType)`: Click parameter type for the `--cert` option, supporting file paths, `'adhoc'` certificates, or SSLContext objects.
  - `__init__(self) -> None`:
  Initializes an instance of a custom Click parameter type (likely a subclass of `click.ParamType`) for SSL certificate paths.  
  - `convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> Any`:
  Converts the input value provided to a Click command into a valid SSL certificate object or path.  

- `_validate_key(ctx: click.Context, param: click.Parameter, value: t.Any) -> t.Any`: Validates the `--key` option in conjunction with `--cert`, ensuring proper usage.

- `SeparatedPathType(click.Path)`: Click parameter type that accepts a list of paths separated by the OS path separator, validating each item as a path.
  - `convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> Any`:
  Converts a CLI input value into a list of processed items. 

- `run_command(...)`: CLI command that runs a local Flask development server with options for host, port, reloader, debugger, threads, SSL, and extra files. Includes original description.

- `shell_command()`: CLI command to start an interactive Python shell within the Flask application context. Includes original description.

- `routes_command(sort: str, all_methods: bool)`: CLI command to display all registered routes of a Flask application, including methods, subdomain/host, and endpoint. Includes original description.

- `main() -> None`: Entrypoint function to invoke the `FlaskGroup` CLI.

`config.py` :

- `ConfigAttribute(name, get_converter=None)`: A descriptor that forwards attribute access to a configuration dictionary, optionally applying a converter function to the retrieved value.

  - `__init__(self, name: str, get_converter: Callable[[Any], T] | None = None) -> None`:
  Initializes the descriptor with a configuration key name and an optional converter function.

  - `__get__(self, obj: App | None, owner: type[App] | None = None) -> T | Self`:
  Retrieves the value from the application's configuration dictionary under the specified key.
  
  - `__set__(obj, value)`: Sets the value in the config for the given attribute name.

- `Config(dict)`: A dictionary-like class that stores configuration values and provides methods to populate them from files, objects, or environment variables.

  - `__init__(self, root_path: str | os.PathLike[str], defaults: dict[str, Any] | None = None) -> None`:
  Initializes the configuration object with a root path and optional default values.

  - `from_envvar(variable_name, silent=False)`: Loads a configuration from a file path stored in the specified environment variable. Raises an error if the variable is not set unless `silent` is `True`.
  
  - `from_prefixed_env(prefix='FLASK', *, loads=json.loads)`: Loads configuration values from environment variables that start with a given prefix. Supports nested keys separated by double underscores and applies a conversion function to the values.
  
  - `from_pyfile(filename, silent=False)`: Loads configuration values from a Python file relative to `root_path`. Only uppercase attributes are added to the config. Fails silently if `silent` is `True` and the file is missing.
  
  - `from_object(obj)`: Loads configuration values from an object or import path. Only uppercase attributes of the object are added to the config.
  
  - `from_file(filename, load, silent=False, text=True)`: Loads configuration from a file using a custom loader function. Supports text or binary modes and optionally ignores missing files.
  
  - `from_mapping(mapping=None, **kwargs)`: Updates the configuration from a dictionary or keyword arguments. Only keys that are uppercase are added. Always returns `True`.
  
  - `get_namespace(namespace, lowercase=True, trim_namespace=True)`: Returns a subset of configuration options that start with the given namespace. Keys can be lowercased and trimmed of the namespace.
  
  - `__repr__()`: Returns a string representation of the `Config` object showing its type and current dictionary contents.

`ctx.py` :

- `_AppCtxGlobals`: A plain object used as a namespace for storing data during an application context. Provides dictionary-like access to attributes.

  - `__getattr__(name)`: Returns the value of the named attribute, raises `AttributeError` if not present.
  
  - `__setattr__(name, value)`: Sets an attribute with the given name and value.
  
  - `__delattr__(name)`: Deletes the named attribute, raises `AttributeError` if not present.
  
  - `get(name, default=None)`: Returns the value of the named attribute or a default if it does not exist.
  
  - `pop(name, default=_sentinel)`: Removes and returns the named attribute, or returns the default if provided.
  
  - `setdefault(name, default=None)`: Returns the value of the named attribute if present, otherwise sets it to a default value.
  
  - `__contains__(item)`: Checks if an attribute exists in the namespace.
  
  - `__iter__()`: Returns an iterator over the attribute names.
  
  - `__repr__()`: Returns a string representation of the `g` proxy for the current app context.

- `after_this_request(f)`: Decorator to register a function to run after the current request. Only works inside a request context.

- `copy_current_request_context(f)`: Decorator to copy the current request context to a new function, typically for use in background tasks.

- `has_request_context()`: Returns `True` if a request context is active, otherwise `False`.

- `has_app_context()`: Returns `True` if an app context is active, otherwise `False`.

- `AppContext(app, *, request=None, session=None)`: Represents an application or request context. Manages `g`, `request`, `session`, URL adapter, and teardown functions.

  - `from_environ(app, environ)`: Creates a new `AppContext` with a request object constructed from a WSGI enviro_
  - `has_request(self) -> bool` : Property that returns `True` if this context was created with request data.
  - `copy(self) -> AppContext`  
  Creates a new `AppContext` with the same internal data (request and session).  
  Useful for copying contexts in asynchronous or threaded environments.  
  - `request(self) -> Request`  
  Property to access the `Request` object associated with this context. Raises `RuntimeError` if no request data exists.

- `session(self) -> SessionMixin`  
  Property to access the session object associated with this context. Lazily loads the session if needed. Raises `RuntimeError` if no request exists.

- `match_request(self) -> None`  
  Performs routing for the current request, storing either the matched endpoint and arguments, or a routing exception in the request object.

- `push(self) -> None`  
  Activates this context as the current one. If a request is present, performs routing. Multiple pushes are tracked and only trigger routing/signals once.

- `pop(self, exc: BaseException | None = None) -> None`  
  Deactivates this context. Calls teardown functions for the request and app context.

  - `__enter__(self) -> AppContext`  
  Context manager entry: pushes the context.  

- `__exit__(self, exc_type, exc_value, tb) -> None`  
  Context manager exit: pops the context and passes any exception to teardown functions.

- `__repr__(self) -> str`  
  Returns a string representation of the context, including the request method and URL if available.

- `__getattr__(name: str) -> Any`  
  Provides backward compatibility for the deprecated `RequestContext`. Emits a `DeprecationWarning` if accessed.

`debughelpers.py` :

- `UnexpectedUnicodeError`: An exception raised to provide better error reporting for unexpected unicode or binary data.

- `DebugFilesKeyError(request, key)`: Raised when accessing a missing key in `request.files` during debugging, providing a detailed error about the `enctype` of the form.

  - `__str__()`: Returns the detailed error message.

- `FormDataRoutingRedirect(request)`: Raised in debug mode when a routing redirect would cause the browser to drop the request method or body (non-GET/HEAD/OPTIONS with status other than 307/308).

- `attach_enctype_error_multidict(request)`: Patches `request.files.__getitem__` to raise a descriptive error about missing `enctype="multipart/form-data"` when accessing files.

- `_dump_loader_info(loader)`: Yields string representations of public attributes of a Jinja2 template loader, including class name and simple attribute values.

- `explain_template_loading_attempts(app, template, attempts)`: Logs detailed information about failed attempts to load a template, helping developers debug missing or mislocated templates. Reports which loader was tried, what was found, and hints about blueprint template placement.

`globals.py` :

- `__getattr__(name)`: Provides a deprecated alias for `request_ctx` with a warning; raises `AttributeError` for other attributes.

`helpers.py`:

- `get_debug_flag()`: Get whether debug mode should be enabled for the app, indicated by the `FLASK_DEBUG` environment variable. Returns `True` if the environment variable is set to a truthy value, otherwise `False`.

- `get_load_dotenv(default=True)`: Determines whether Flask should load default `.env` files, controlled by the `FLASK_SKIP_DOTENV` environment variable. Returns a boolean, defaulting to the provided `default` value.

- `stream_with_context(generator_or_function: t.Iterator[t.AnyStr]) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]`:  
  Wraps a response generator or generator function so that it executes inside the current Flask request context. This ensures that `request`, `session`, and `g` are available when the generator runs, even if the original request context has ended. Wraps a response generator function so that it runs inside the current request context, preserving access to `request`, `session`, and other context globals. Can be used as a decorator or to wrap an existing generator.
  - `generator() -> Iterator[AnyStr]`: An internal generator used by `stream_with_context`.  Ensures that a Flask application/request context is active before running.

- `make_response(*args)`: Converts a return value from a view function into a `Response` object. Allows headers to be added and supports multiple return types including single values, tuples, or nothing.

- `url_for(endpoint, *, _anchor=None, _method=None, _scheme=None, _external=None, **values)`: Generates a URL to a given endpoint using the current application context. Supports optional anchor, method, scheme, and external URL generation.

- `redirect(location, code=302, Response=None)`: Creates a redirect `Response` object. Uses the current app’s redirect method if available; otherwise falls back to Werkzeug’s default.

- `abort(code, *args, **kwargs)`: Raises an HTTP exception with the given status code, using the current app’s aborter if available, or Werkzeug’s `abort` otherwise.

- `get_template_attribute(template_name, attribute)`: Loads a macro or variable exported by a template, allowing Python code to invoke it directly.

- `flash(message, category="message")`: Flashes a message to the next request, storing it in the session. Supports categorization of messages.

- `get_flashed_messages(with_categories=False, category_filter=())`: Retrieves flashed messages from the session, optionally returning message-category tuples and/or filtering by category.

- `_prepare_send_file_kwargs(**kwargs)`: Internal helper to prepare keyword arguments for `send_file` and `send_from_directory`, setting defaults based on the current request context.

- `send_file(path_or_file, mimetype=None, as_attachment=False, download_name=None, conditional=True, etag=True, last_modified=None, max_age=None)`: Sends a file to the client. Accepts file paths or file-like objects and supports various options including MIME type, conditional requests, and caching.

- `send_from_directory(directory, path, **kwargs)`: Sends a file from a specific directory securely, using `send_file`. Ensures the file path is safe and relative to the given directory.

- `get_root_path(import_name)`: Finds the root path of a package or module. Returns the directory containing the module file or the current working directory if the module path cannot be determined.

- `_split_blueprint_path(name)`: Internal helper that recursively splits a dotted blueprint name into a list of hierarchical components. Cached for performance.

`logging.py`:

- `wsgi_errors_stream()`: A `LocalProxy` property that returns the most appropriate error stream for logging. Uses `request.environ["wsgi.errors"]` if a request context is active; otherwise defaults to `sys.stderr`. Recommended for use in custom `logging.StreamHandler`.

- `has_level_handler(logger: logging.Logger) -> bool`: Checks whether a given logger or any of its ancestor loggers has a handler that will process messages at the logger’s effective level. Returns `True` if such a handler exists, otherwise `False`.

- `create_logger(app: App) -> logging.Logger`: Returns the logger for the given Flask `app`, configuring it if necessary. Sets the log level to `DEBUG` if the app is in debug mode and no level is already set. Adds `default_handler` if no handler exists for the effective level.

`session.py`:

- `SessionMixin(MutableMapping[str, t.Any])`: Mixin class providing session-specific attributes for dictionary-like objects.
  - `permanent(self) -> bool`:  
  A property that reflects the `"_permanent"` key in the session dictionary. It indicates whether the session is permanent (i.e., should persist beyond the browser session).
  - `permanent(self, value: bool) -> None`:  
  Setter for the `permanent` property. Updates the `"_permanent"` key in the session dictionary based on the given boolean value.

- `SecureCookieSession(CallbackDict[str, t.Any], SessionMixin)`: Session class backed by signed cookies.
  - `__init__(self, initial: Mapping[str, Any] | Iterable[tuple[str, Any]] | None = None) -> None`:  
  Initializes a session dictionary with optional initial data. Tracks access and modification events to manage session state.  

  - `__getitem__(self, key: str) -> Any`:  
  Overrides dictionary access to mark the session as accessed whenever a key is retrieved.

  - `get(self, key: str, default: Any = None) -> Any`:  
  Overrides the `get` method to mark the session as accessed when a key is queried.  

  - `setdefault(self, key: str, default: Any = None) -> Any`:  
  Overrides `setdefault` to mark the session as accessed when a key is queried or added. 


- `NullSession(SecureCookieSession)`: Read-only session used when session support is unavailable. Raises a runtime error on any modification attempt.
  - `_fail(self, *args: Any, **kwargs: Any) -> NoReturn`:  
  Internal helper method that raises a `RuntimeError` indicating the session is unavailable due to a missing secret key.  


- `SessionInterface`: Base interface for custom session backends.
  - `make_null_session(app: Flask) -> NullSession`: Returns a null session instance.
  - `is_null_session(obj: object) -> bool`: Checks if an object is a null session.
  - `get_cookie_name(app: Flask) -> str`: Returns the name of the session cookie.
  - `get_cookie_domain(app: Flask) -> str | None`: Returns the cookie domain.
  - `get_cookie_path(app: Flask) -> str`: Returns the cookie path.
  - `get_cookie_httponly(app: Flask) -> bool`: Returns whether the cookie is HttpOnly.
  - `get_cookie_secure(app: Flask) -> bool`: Returns whether the cookie is secure.
  - `get_cookie_samesite(app: Flask) -> str | None`: Returns the cookie SameSite attribute.
  - `get_cookie_partitioned(app: Flask) -> bool`: Returns whether the cookie is partitioned.
  - `get_expiration_time(app: Flask, session: SessionMixin) -> datetime | None`: Returns expiration time for the session.
  - `should_set_cookie(app: Flask, session: SessionMixin) -> bool`: Determines whether a `Set-Cookie` header should be set.
  - `open_session(app: Flask, request: Request) -> SessionMixin | None`: Opens and returns a session object.
  - `save_session(app: Flask, session: SessionMixin, response: Response) -> None`: Saves the session into the response.

- `_lazy_sha1(string: bytes = b"") -> t.Any`: Lazily returns a `hashlib.sha1` object. Used to avoid import issues in FIPS builds.

- `SecureCookieSessionInterface(SessionInterface)`: Default session interface storing sessions in signed cookies using `itsdangerous`.
  - `get_signing_serializer(app: Flask) -> URLSafeTimedSerializer | None`: Returns a signing serializer or `None` if `secret_key` is not set.
  - `open_session(app: Flask, request: Request) -> SecureCookieSession | None`: Loads session from cookie, returns empty session on failure.
  - `save_session(app: Flask, session: SessionMixin, response: Response) -> None`: Writes session cookie to response if necessary, deletes if empty.

`signals.py`:

- This module defines Flask’s built-in application and request lifecycle signals, using the `blinker` library to allow different parts of an application (or extensions) to communicate through events. Each signal represents a specific stage in the request or application context, enabling developers to hook custom logic without modifying core Flask behavior.

`templating.py` :

- `_default_template_ctx_processor()`: Default template context processor. Injects `request`, `session`, and `g` into the template context if a request context is active.

- `Environment(app, **options)`: Subclass of `jinja2.Environment` that integrates Flask application and blueprint awareness. Automatically sets the loader from the application's global Jinja loader if none is provided.

- `DispatchingJinjaLoader(app)`: A loader that searches for templates in the application and all registered blueprint folders. Supports optional debug mode to explain template loading attempts.

  - `get_source(environment, template)`: Retrieves the template source code. Chooses between explained or fast lookup depending on `EXPLAIN_TEMPLATE_LOADING` config.
  
  - `_get_source_explained(environment, template)`: Iterates over all loaders and explains which attempts were made to find a template when debug mode is enabled.
  
  - `_get_source_fast(environment, template)`: Quickly iterates over all loaders and returns the first found template; raises `TemplateNotFound` if none is found.
  
  - `_iter_loaders(template)`: Yields tuples of `(source_object, loader)` for the application and all blueprints that have a loader.
  
  - `list_templates()`: Returns a list of all template names available in the application and its blueprints.

- `_render(app, template, context)`: Internal helper to render a Jinja template with the given context, sending Flask signals `before_render_template` and `template_rendered`.

- `render_template(template_name_or_list, **context)`: Render a template by name (or list of names) with the given context. Returns a fully rendered string.

- `render_template_string(source, **context)`: Render a template from a given source string with the provided context. Returns the rendered string.

- `_stream(app, template, context)`: Internal helper that streams a template's rendered content as an iterator. Sends `before_render_template` and `template_rendered` signals appropriately.

- `stream_template(template_name_or_list, **context)`: Render a template by name (or list of names) as a stream. Returns an iterator of strings suitable for streaming responses.

- `stream_template_string(source, **context)`: Render a template from a source string as a stream. Returns an iterator of strings suitable for streaming responses.

`testing.py` :

- `EnvironBuilder(app, path='/', base_url=None, subdomain=None, url_scheme=None, *args, **kwargs)`: Subclass of `werkzeug.test.EnvironBuilder` that takes defaults from a Flask application. Automatically constructs `base_url` and applies app-specific configuration like `SERVER_NAME`, `APPLICATION_ROOT`, and `PREFERRED_URL_SCHEME`.

  - `json_dumps(obj, **kwargs)`: Serialize a Python object to a JSON string according to the Flask app's JSON configuration.

- `_get_werkzeug_version()`: Returns the installed Werkzeug version, caching the result for efficiency.

- `FlaskClient(Client)`: A test client for Flask that extends Werkzeug's `Client` with Flask-specific behavior, including support for session transactions and preserving request contexts.

  - `session_transaction(*args, **kwargs)`: Context manager to open a session transaction for modifying the session during tests. Automatically saves the session back when exiting the block.
  
  - `_copy_environ(other)`: Returns a copy of the WSGI environment combined with the client's base environment, optionally preserving context.
  
  - `_request_from_builder_args(args, kwargs)`: Helper to create a `BaseRequest` from arguments passed to the client, using `EnvironBuilder`.
  
  - `open(*args, buffered=False, follow_redirects=False, **kwargs)`: Sends a request to the application, returning a `TestResponse`. Handles Flask-specific features like context preservation and JSON response integration.
  
  - `__enter__()`: Enables context manager usage for preserving request contexts across multiple client calls.
  
  - `__exit__(exc_type, exc_value, tb)`: Ends the context manager, closing preserved contexts.

- `FlaskCliRunner(CliRunner)`: A `click.testing.CliRunner` subclass for testing Flask CLI commands.

  - `invoke(cli=None, args=None, **kwargs)`: Invokes a CLI command in an isolated environment. Automatically provides a `ScriptInfo` object for the Flask app if `obj` is not given, allowing testing of app CLI commands.

`typing.py` :

- This module defines type aliases and callable signatures used throughout Flask to ensure consistent type checking, static analysis, and better IDE support. It describes the expected input and output types for core Flask components such as views, request hooks, error handlers, and template processors.

`views.py` :

- `View`: Base class for creating class-based views. Subclasses should override `dispatch_request` to define the view logic. Use `as_view` to convert the class into a view function suitable for URL routing.

  - `dispatch_request()`: Must be overridden by subclasses to handle the request and return a valid response. URL variables are passed as keyword arguments.
  
  - `as_view(name, *class_args, **class_kwargs)`: Class method that converts the view class into a callable view function. Handles instantiation per request (or single instance if `init_every_request` is `False`) and applies any class-level decorators. Attaches metadata such as `view_class`, `methods`, and `provide_automatic_options` to the generated view function.

- `MethodView(View)`: Extends `View` to automatically dispatch HTTP methods to corresponding instance methods (`get`, `post`, `put`, etc.). Useful for building RESTful APIs.

  - `__init_subclass__(**kwargs)`: Automatically sets the `methods` attribute based on the HTTP method functions implemented on the class, inheriting methods from base classes as needed.

  - `dispatch_request(**kwargs)`: Looks up the method corresponding to the current request's HTTP method and calls it. If the request is `HEAD` and no handler exists, falls back to `get`. Raises an assertion error if no suitable method is found.

`wrappers.py` :

- `Request(RequestBase)`: The default request object in Flask. Subclasses `werkzeug.wrappers.Request` and adds Flask-specific attributes and behavior, such as `url_rule`, `view_args`, and blueprint handling.

  - `max_content_length`: Property to get or set the maximum number of bytes to read from the request. Defaults to the Flask app's `MAX_CONTENT_LENGTH` config. Raises `RequestEntityTooLarge` if exceeded.
  
  - `max_form_memory_size`: Property to get or set the maximum size of non-file form fields in a `multipart/form-data` request. Defaults to `MAX_FORM_MEMORY_SIZE` from the app config.
  
  - `max_form_parts`: Property to get or set the maximum number of fields allowed in a `multipart/form-data` request. Defaults to `MAX_FORM_PARTS` from the app config.
  
  - `endpoint`: Returns the endpoint that matched the request URL or `None` if matching failed.
  
  - `blueprint`: Returns the name of the current blueprint, or `None` if not part of a blueprint or matching failed.
  
  - `blueprints`: Returns a list of blueprint names from the current blueprint up through parent blueprints. Returns an empty list if no blueprint is active.
  
  - `_load_form_data()`: Loads form data and applies Flask-specific debug enhancements for non-multipart forms in debug mode.
  
  - `on_json_loading_failed(e)`: Handles JSON decoding errors. In debug mode, re-raises the original exception; otherwise, raises a generic `BadRequest`.

- `Response(ResponseBase)`: The default response object in Flask. Subclasses `werkzeug.wrappers.Response` with default HTML mimetype and JSON support.
  
  - `max_cookie_size`: Read-only property that returns the app's `MAX_COOKIE_SIZE` configuration or Werkzeug's default if outside an app context.

## flask/json/:
`__init__.py` :

- `dumps(obj, **kwargs)`: Serialize a Python object to a JSON-formatted string. If `current_app` is available, it uses the app's JSON provider; otherwise, it falls back to `json.dumps`. Supports custom serialization via the `default` parameter.

- `dump(obj, fp, **kwargs)`: Serialize a Python object as JSON and write it to a file-like object `fp`. Uses the app's JSON provider if `current_app` is available, otherwise falls back to `json.dump`.

- `loads(s, **kwargs)`: Deserialize a JSON-formatted string or bytes into a Python object. If `current_app` is available, it uses the app's JSON provider; otherwise, it uses `json.loads`.

- `load(fp, **kwargs)`: Deserialize JSON content from a file-like object `fp` into a Python object. Uses the app's JSON provider if `current_app` is available, otherwise falls back to `json.load`.

- `jsonify(*args, **kwargs)`: Serialize the given arguments into a JSON response and return a `Response` object with the `application/json` mimetype. Requires an active app context and delegates to the app's JSON provider. Supports formatting in debug mode and serialization of `decimal.Decimal`.

`provider.py` :

- `JSONProvider(app: App)`: A base class providing a standard set of JSON operations for a Flask application. Subclasses can customize JSON behavior or use different JSON libraries. Stores a weak reference to the application instance.

  - `dumps(obj, **kwargs)`: Serialize a Python object to a JSON string. Must be implemented by subclasses.

  - `dump(obj, fp, **kwargs)`: Serialize a Python object as JSON and write it to a file-like object. Uses `dumps` internally.

  - `loads(s, **kwargs)`: Deserialize a JSON string or bytes into a Python object. Must be implemented by subclasses.

  - `load(fp, **kwargs)`: Deserialize JSON content from a file-like object into a Python object. Uses `loads` internally.

  - `_prepare_response_obj(args, kwargs)`: Helper method to prepare the object to serialize for a JSON response. Ensures either positional or keyword arguments are used, not both, and returns the appropriate object.

  - `response(*args, **kwargs)`: Serialize the given arguments as JSON and return a `Response` object with the `application/json` mimetype. Uses `_prepare_response_obj` to determine the object to serialize.

- `_default(o)`: A helper function to provide default serialization for objects not natively supported by JSON. Handles `date`, `decimal.Decimal`, `uuid.UUID`, dataclasses, and objects with a `__html__` method.

- `DefaultJSONProvider(JSONProvider)`: A concrete implementation of `JSONProvider` using Python's built-in `json` library. Adds support for additional data types and provides configurable serialization options.

  - `dumps(obj, **kwargs)`: Serialize data as JSON using Python's `json.dumps`. Uses `default`, `ensure_ascii`, and `sort_keys` attributes by default.

  - `loads(s, **kwargs)`: Deserialize JSON data from a string or bytes using Python's `json.loads`.

  - `response(*args, **kwargs)`: Serialize the given arguments as JSON and return a `Response` object with the configured MIME type. Respects `compact` and debug mode for formatting.

`tag.py` :

- `JSONTag(serializer: TaggedJSONSerializer)`: Base class for defining type tags used by `TaggedJSONSerializer`. Subclasses define how non-standard JSON types are serialized and deserialized.

  - `check(value)`: Determine if the given value should be tagged by this tag. Must be implemented by subclasses.

  - `to_json(value)`: Convert a Python object to a JSON-compatible representation. Must be implemented by subclasses.

- `TagDict(JSONTag)`: Handles 1-item dictionaries whose key matches a registered tag. Suffixes the key with `__` when serializing and removes it when deserializing.
  - `check(self, value: Any) -> bool`:  
    Determines whether the given value qualifies for this tag — i.e., it is a dictionary with exactly one key, and that key matches a registered tag in the serializer.

  - `to_json(self, value: Any) -> Any`:  
    Converts a matching one-key dictionary into its tagged JSON representation.  
    Appends `"__"` to the key and applies the serializer’s tagging mechanism to the value.

  - `to_python(self, value: Any) -> Any`:  
    Reverses the tagging applied by `to_json`, removing the `"__"` suffix from the key and restoring the original single-key dictionary structure.

- `PassDict(JSONTag)`: Handles standard dictionaries, recursively tagging their values without altering the keys.
  - `check(self, value: Any) -> bool`:  
    Checks whether the provided value is a dictionary.  
    Returns `True` for all `dict` instances, indicating that this tag can handle standard dictionaries.

  - `to_json(self, value: Any) -> Any`:  
    Serializes the dictionary by applying the serializer’s `tag()` method recursively to each value.  
    Keys are preserved as-is since they must already be strings in valid JSON objects.

- `TagTuple(JSONTag)`: Handles tuples by converting them to lists of tagged elements for JSON serialization.
  - `check(self, value: Any) -> bool`:  
    Determines if the given value is a tuple.  
    Returns `True` for all instances of `tuple`.

  - `to_json(self, value: Any) -> Any`:  
    Serializes a tuple into a JSON-compatible list, applying the serializer’s `tag()` method to each element recursively.

  - `to_python(self, value: Any) -> Any`:  
    Deserializes the list representation back into a tuple, restoring the original data type.

- `PassList(JSONTag)`: Handles lists by recursively tagging each element.
  - `check(value: Any) -> bool`: Returns `True` if `value` is a list.  
  - `to_json(value: Any) -> Any`: Serializes each list item using the serializer’s `tag()` method.

- `TagBytes(JSONTag)`: Handles bytes by encoding them to a base64 ASCII string for JSON, and decodes them back when deserializing.
  - `check(value: Any) -> bool`: Returns `True` if `value` is a `bytes` object.  
  - `to_json(value: Any) -> Any`: Encodes bytes to a Base64 ASCII string.  
  - `to_python(value: Any) -> Any`: Decodes Base64 strings back into raw bytes.


- `TagMarkup(JSONTag)`: Handles objects with a `__html__` method (e.g., `markupsafe.Markup`) by serializing to a string and deserializing back to a `Markup` object.
  - `check(value: Any) -> bool`: Returns `True` if the object has a callable `__html__` method.  
  - `to_json(value: Any) -> Any`: Calls `value.__html__()` and serializes the resulting string.  
  - `to_python(value: Any) -> Any`: Converts the serialized value back to a `Markup` instance.

- `TagUUID(JSONTag)`: Handles `uuid.UUID` objects by serializing to hexadecimal string and deserializing back to `UUID`.
  - `check(value: Any) -> bool`: Returns `True` if `value` is a `UUID` instance.  
  - `to_json(value: Any) -> Any`: Converts a UUID to its `.hex` representation.  
  - `to_python(value: Any) -> Any`: Restores the `UUID` from its hex string.


- `TagDateTime(JSONTag)`: Handles `datetime.datetime` objects by serializing to HTTP date string and deserializing back to `datetime`.
  - `check(value: Any) -> bool`: Returns `True` if `value` is a `datetime` instance.  
  - `to_json(value: Any) -> Any`: Formats the datetime using HTTP date formatting (`http_date`).  
  - `to_python(value: Any) -> Any`: Parses an HTTP date string back into a `datetime` object.

- `TaggedJSONSerializer`: Serializer that uses a tag system to represent objects not natively supported by JSON. Supports dict, tuple, list, bytes, Markup, UUID, and datetime types by default.

  - `register(tag_class, force=False, index=None)`: Register a new `JSONTag` subclass with the serializer. Can insert at a specific position in the order and optionally overwrite existing tags.

  - `tag(value)`: Convert a value to a tagged representation if necessary using the registered tags.

  - `untag(value)`: Convert a tagged representation back to the original Python type.

  - `_untag_scan(value)`: Recursively untag nested structures (lists and dictionaries).

  - `dumps(value)`: Serialize a Python object to a compact JSON string, applying tags as needed.

  - `loads(value)`: Deserialize a JSON string, restoring any tagged objects.

## flask/sansio/:
`app.py`:

- `_make_timedelta(value: timedelta | int | None) -> timedelta | None`:  
  Converts an integer or `timedelta` to a `timedelta` object. If the value is already `None` or a `timedelta`, it is returned as is.

- `App(Scaffold)`:  
  The main Flask application class implementing a WSGI application and central registry for routes, templates, configurations, and blueprints.

  - `__init__(self, import_name, static_url_path=None, static_folder='static', static_host=None, host_matching=False, subdomain_matching=False, template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None)`:  
    Initializes a new Flask application instance. Sets up paths, configuration, JSON provider, URL map, and internal state for blueprints, extensions, and teardown functions.

  - `_check_setup_finished(self, f_name: str) -> None`:  
    Raises an `AssertionError` if a setup method is called after the application has handled its first request.

  - `name(self) -> str`:  
    Returns the name of the application, usually derived from the import name or the main script filename.

  - `logger(self) -> logging.Logger`:  
    Returns a standard Python logger for the application. Configures default handlers and debug-level logging if necessary.

  - `jinja_env(self) -> Environment`:  
    Returns the Jinja environment used to load templates. Created on first access.

  - `create_jinja_environment(self) -> Environment`:  
    Raises `NotImplementedError`. Intended to be overridden to create a custom Jinja environment.

  - `make_config(self, instance_relative: bool = False) -> Config`:  
    Creates the application configuration object (`Config`) using defaults and the debug flag.

  - `make_aborter(self) -> Aborter`:  
    Creates an `Aborter` instance used by `flask.abort` to raise HTTP exceptions.

  - `auto_find_instance_path(self) -> str`:  
    Determines the default instance folder path if not explicitly provided.

  - `create_global_jinja_loader(self) -> DispatchingJinjaLoader`:  
    Creates a loader that dispatches between application and blueprint Jinja loaders.

  - `select_jinja_autoescape(self, filename: str) -> bool`:  
    Determines whether autoescaping should be active for a given template filename.

  - `debug(self) -> bool`:  
    Property that returns the value of the `DEBUG` configuration key.

  - `debug(self, value: bool) -> None`:  
    Setter for the `debug` property. Updates the config and optionally enables template auto-reload.

  - `register_blueprint(self, blueprint: Blueprint, **options: t.Any) -> None`:  
    Registers a blueprint on the application. Calls the blueprint’s `register` method and stores it in `blueprints`.

  - `iter_blueprints(self) -> t.ValuesView[Blueprint]`:  
    Iterates over all registered blueprints in registration order.

  - `add_url_rule(self, rule: str, endpoint: str | None = None, view_func: ft.RouteCallable | None = None, provide_automatic_options: bool | None = None, **options: t.Any) -> None`:  
    Adds a URL rule to the application, associating it with a view function and endpoint. Handles automatic HTTP methods and OPTIONS logic.

  - `template_filter(self, name: T_template_filter | str | None = None) -> T_template_filter | t.Callable[[T_template_filter], T_template_filter]`:  
    Decorator to register a function as a custom Jinja filter.

  - `add_template_filter(self, f: ft.TemplateFilterCallable, name: str | None = None) -> None`:  
    Registers a function as a Jinja template filter.

  - `template_test(self, name: T_template_test | str | None = None) -> T_template_test | t.Callable[[T_template_test], T_template_test]`:  
    Decorator to register a function as a custom Jinja test.

  - `add_template_test(self, f: ft.TemplateTestCallable, name: str | None = None) -> None`:  
    Registers a function as a Jinja template test.

  - `template_global(self, name: T_template_global | str | None = None) -> T_template_global | t.Callable[[T_template_global], T_template_global]`:  
    Decorator to register a function as a custom Jinja global.

  - `add_template_global(self, f: ft.TemplateGlobalCallable, name: str | None = None) -> None`:  
    Registers a function as a Jinja global.

  - `teardown_appcontext(self, f: T_teardown) -> T_teardown`:  
    Registers a function to be called when the application context is popped.

  - `shell_context_processor(self, f: T_shell_context_processor) -> T_shell_context_processor`:  
    Registers a shell context processor function.

  - `_find_error_handler(self, e: Exception, blueprints: list[str]) -> ft.ErrorHandlerCallable | None`:  
    Finds an appropriate error handler for a given exception and blueprint hierarchy.

  - `trap_http_exception(self, e: Exception) -> bool`:  
    Determines whether an HTTP exception should be trapped for debugging purposes.

  - `should_ignore_error(self, error: BaseException | None) -> bool`:  
    Determines if a teardown error should be ignored.

  - `redirect(self, location: str, code: int = 302) -> BaseResponse`:  
    Creates a redirect response object using Werkzeug.

  - `inject_url_defaults(self, endpoint: str, values: dict[str, t.Any]) -> None`:  
    Injects default URL values for a given endpoint into the `values` dictionary.

  - `handle_url_build_error(self, error: BuildError, endpoint: str, values: dict[str, t.Any]) -> str`:  
    Handles `BuildError` exceptions raised by `url_for`. Calls `url_build_error_handlers` and returns a resolved URL if possible.

`blueprints.py`:

- `BlueprintSetupState(blueprint, app, options, first_registration)`: A temporary holder object for registering a blueprint with an application. It stores references to the blueprint, the app, URL defaults, subdomain, and URL prefix.

  - `add_url_rule(rule, endpoint=None, view_func=None, **options)`: Helper method to register a URL rule (and optionally a view function) on the application. The endpoint is automatically prefixed with the blueprint’s name.

- `Blueprint(name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None, root_path=None, cli_group=_sentinel)`: Represents a blueprint, a collection of routes and related functions that can be registered later on a Flask application.

  - `_check_setup_finished(f_name)`: Ensures that a setup method cannot be called after the blueprint has been registered at least once.

  - `record(func)`: Registers a function to be called when the blueprint is registered on the application. The function receives a `BlueprintSetupState` object as argument.

  - `record_once(func)`: Similar to `record`, but ensures the function is only called the first time the blueprint is registered.

  - `make_setup_state(app, options, first_registration=False)`: Creates a `BlueprintSetupState` object, which is passed to all deferred functions when the blueprint is registered.

  - `register_blueprint(blueprint, **options)`: Registers a nested blueprint on this blueprint. Options can override defaults of the nested blueprint.

  - `register(app, options)`: Called by `Flask.register_blueprint` to register all views and callbacks of this blueprint with the application. Also registers nested blueprints and CLI commands.

  - `_merge_blueprint_funcs(app, name)`: Merges this blueprint’s view functions, error handlers, request hooks, and template-related functions into the parent application.

  - `add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options)`: Registers a URL rule with the blueprint. The URL is prefixed with the blueprint’s URL prefix, and the endpoint is prefixed with the blueprint’s name.

  - `app_template_filter(name)`: Decorator to register a function as a global Jinja template filter available in all templates. The name is optional.

  - `add_app_template_filter(f, name=None)`: Registers a function as a global Jinja template filter.

  - `app_template_test(name)`: Decorator to register a function as a global Jinja template test available in all templates. The name is optional.

  - `add_app_template_test(f, name=None)`: Registers a function as a global Jinja template test.

  - `app_template_global(name)`: Decorator to register a function as a global Jinja template global available in all templates. The name is optional.

  - `add_app_template_global(f, name=None)`: Registers a function as a global Jinja template global.

  - `before_app_request(f)`: Decorator to register a function as a request hook executed before every request, not just requests handled by the blueprint.

  - `after_app_request(f)`: Decorator to register a function as a request hook executed after every request, not just requests handled by the blueprint.

  - `teardown_app_request(f)`: Decorator to register a function as a request teardown hook executed after every request, not just requests handled by the blueprint.

  - `app_context_processor(f)`: Decorator to register a function as a template context processor for templates rendered by every view, not just blueprint views.

  - `app_errorhandler(code)`: Decorator to register an error handler for all requests matching a specific exception type or HTTP status code, not just blueprint requests.

  - `app_url_value_preprocessor(f)`: Decorator to register a function that preprocesses URL values for all requests, not just blueprint requests.

  - `app_url_defaults(f)`: Decorator to register a function that provides default URL values for all requests, not just blueprint requests.

`scaffold.py`:

* `setupmethod(f: F) -> F`: A decorator for methods of `Scaffold` that ensures the setup process is finished before the method is called. Raises an error if called before setup is complete.

* `class Scaffold`: Base class for objects like `Flask` and `Blueprint` that provides common behavior for routing, template handling, static files, and request lifecycle hooks.

  * `__init__(import_name, static_folder=None, static_url_path=None, template_folder=None, root_path=None)`: Initializes a scaffold with the given import name, static folder, template folder, and root path. Sets up internal data structures for routing, error handling, and request lifecycle functions.

  * `__repr__() -> str`: Returns a string representation of the scaffold, including its class name and `name` attribute.

  * `_check_setup_finished(f_name: str) -> None`: Placeholder method to check whether the setup is finished. Must be implemented in subclasses.

  * `static_folder` (property): Returns the absolute path to the configured static folder. `None` if not set.

  * `static_folder` (setter): Sets the static folder path, normalizing it to a string.

  * `has_static_folder` (property): Returns `True` if a static folder is configured.

  * `static_url_path` (property): Returns the URL path to serve static files. Derived from `static_folder` if not explicitly set.

  * `static_url_path` (setter): Sets the static URL path, removing trailing slashes.

  * `jinja_loader` (cached_property): Returns a `jinja2.FileSystemLoader` for the template folder if set, or `None`.

  * `_method_route(method: str, rule: str, options: dict[str, Any]) -> Callable`: Internal helper to create a route decorator for a single HTTP method.

  * `get(rule: str, **options) -> Callable`: Shortcut for registering a route with the `GET` method.

  * `post(rule: str, **options) -> Callable`: Shortcut for registering a route with the `POST` method.

  * `put(rule: str, **options) -> Callable`: Shortcut for registering a route with the `PUT` method.

  * `delete(rule: str, **options) -> Callable`: Shortcut for registering a route with the `DELETE` method.

  * `patch(rule: str, **options) -> Callable`: Shortcut for registering a route with the `PATCH` method.

  * `route(rule: str, **options) -> Callable`: Decorator to register a view function with a URL rule and options. Delegates to `add_url_rule`.

  * `add_url_rule(rule: str, endpoint=None, view_func=None, provide_automatic_options=None, **options)`: Registers a URL rule and associates it with an endpoint and view function. Must be implemented in subclasses.

  * `endpoint(endpoint: str) -> Callable`: Decorator to associate a view function with a given endpoint name.

  * `before_request(f: T_before_request) -> T_before_request`: Registers a function to run before each request.

  * `after_request(f: T_after_request) -> T_after_request`: Registers a function to run after each request, which can modify the response.

  * `teardown_request(f: T_teardown) -> T_teardown`: Registers a function to run at the end of a request context, even if an exception occurred.

  * `context_processor(f: T_template_context_processor) -> T_template_context_processor`: Registers a function to add extra context variables to templates.

  * `url_value_preprocessor(f: T_url_value_preprocessor) -> T_url_value_preprocessor`: Registers a function to preprocess URL values before calling the view function.

  * `url_defaults(f: T_url_defaults) -> T_url_defaults`: Registers a function to modify URL generation defaults before building URLs.

  * `errorhandler(code_or_exception: type[Exception] | int) -> Callable`: Decorator to register a function as an error handler for a given exception class or HTTP status code.

  * `register_error_handler(code_or_exception: type[Exception] | int, f: ft.ErrorHandlerCallable)`: Registers an error handler directly without using a decorator.

  * `_get_exc_class_and_code(exc_class_or_code: type[Exception] | int) -> tuple[type[Exception], int | None]`: Resolves an exception class and its associated HTTP status code.

* `_endpoint_from_view_func(view_func: ft.RouteCallable) -> str`: Returns the default endpoint name for a given view function, which is its `__name__`.

* `_find_package_path(import_name: str) -> str`: Finds the filesystem path containing the specified package or module.

* `find_package(import_name: str) -> tuple[str | None, str]`: Determines the installation prefix and filesystem path for a package. Returns `(prefix, path)`, where `prefix` is `None` if the package is not installed system-wide or in a virtualenv.
