# Architecture Design
Below is a text-based representation of the file tree.
```
├── djangorestframework-simplejwt
│   ├── authentication.py
│   ├── backends.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── locale
│   │   ├── ...
│   ├── models.py
│   ├── serializers.py
│   ├── settings.py
│   ├── state.py
│   ├── token_blacklist
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── management
│   │   │   ├── commands
│   │   │   │   ├── flushexpiredtokens.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_outstandingtoken_jti_hex.py
│   │   │   ├── 0003_auto_20171017_2007.py
│   │   │   ├── 0004_auto_20171017_2013.py
│   │   │   ├── 0005_remove_outstandingtoken_jti.py
│   │   │   ├── 0006_auto_20171017_2113.py
│   │   │   ├── 0007_auto_20171017_2214.py
│   │   │   ├── 0008_migrate_to_bigautofield.py
│   │   │   ├── 0010_fix_migrate_to_bigautofield.py
│   │   │   ├── 0011_linearizes_history.py
│   │   │   ├── 0012_alter_outstandingtoken_user.py
│   │   │   └── __init__.py
│   │   └── models.py
│   ├── tokens.py
│   ├── utils.py
│   └── views.py
```

## rest_framework_simplejwt/token_blacklist/management/:

`__init__.py`:
none

`/commands/__init__.py`:
none

`/commands/flushexpiredtokens.py `:
- `Command(BaseCommand)`:  
  A Django management command class that provides functionality for maintaining the token database in the `rest_framework_simplejwt` system by removing expired tokens.

  - `handle(self, *args, **kwargs)`:  
    Deletes all entries from the `OutstandingToken` model whose `expires_at` timestamp is less than or equal to the current UTC time, effectively flushing expired tokens from the database.

## rest_framework_simplejwt/token_blacklist/migrations/:

`__init__.py`:
none

`0001_initial.py`:

- `Migration(migrations.Migration)`:  
  The initial database migration for the token blacklist app, responsible for creating the necessary database schema to support token tracking and blacklisting functionality.

`0002_outstandingtoken_jti_hex.py `:

- `Migration(migrations.Migration)`:  
  A database migration that extends the `OutstandingToken` model to include an additional field for storing the hexadecimal representation of the token’s unique identifier (JTI).

`0003_auto_20171017_2007.py` :
- `populate_jti_hex(apps, schema_editor)`:  
  A data migration function that populates the new `jti_hex` field in the `OutstandingToken` model by converting each token’s UUID `jti` value into its hexadecimal string representation.  
- `reverse_populate_jti_hex(apps, schema_editor)`:  
  A reverse migration function that restores the `jti` field from its hexadecimal representation (`jti_hex`).  
- `Migration(migrations.Migration)`:  
  Defines the migration that executes the `populate_jti_hex` data transformation.

`0004_auto_20171017_2013.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that updates the `OutstandingToken` model to enforce uniqueness on the `jti_hex` field, ensuring each token’s hexadecimal identifier is distinct in the database.

`0005_remove_outstandingtoken_jti.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that removes the obsolete `jti` field from the `OutstandingToken` model after migrating its data to the new `jti_hex` field.

`0006_auto_20171017_2113.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that renames the `jti_hex` field in the `OutstandingToken` model back to `jti`, reflecting its role as the primary unique identifier for each token.


`0007_auto_20171017_2214.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that relaxes constraints on specific fields of the `OutstandingToken` model, allowing greater flexibility when storing token records without strict user or timestamp requirements.

`0008_use_bigautofield_ids.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that upgrades the primary key fields of the `BlacklistedToken` and `OutstandingToken` models to use `BigAutoField` instead of `AutoField`, improving scalability for large datasets.

`0010_fix_migrate_to_bigautofield.py` :

- `Migration(migrations.Migration)`:  
  A follow-up schema migration that reaffirms the use of `BigAutoField` as the primary key type for both `BlacklistedToken` and `OutstandingToken` models, ensuring consistency with Django 3.2’s default primary key configuration.

`0011_linearizes_history.py` :

- `Migration(migrations.Migration)`:  
  A custom migration script designed to dynamically determine migration dependencies based on the existing migration files in the `token_blacklist` app. This ensures that the migration order remains consistent even if earlier migrations are renamed, reordered, or missing.

`0012_alter_outstandingtoken_user.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that modifies the `user` field behavior in the `OutstandingToken` model to preserve tokens when their associated user accounts are deleted.

`0013_alter_blacklistedtoken_options_and_more.py` :

- `Migration(migrations.Migration)`:  
  A schema migration that enhances the metadata of the `BlacklistedToken` and `OutstandingToken` models by adding human-readable names and ensuring consistent model ordering for administrative and display purposes.

## rest_framework_simplejwt/token_blacklist/：
`__init__.py` :

- `default_app_config`:  
  A conditional configuration declaration that ensures compatibility with Django versions earlier than **3.2**.   

`admin.py` :
- `OutstandingTokenAdmin(admin.ModelAdmin)`:  
  Customizes the Django admin interface for the `OutstandingToken` model, defining how outstanding (non-blacklisted) tokens are displayed and interacted with in the admin panel.  
  - `get_queryset(*args, **kwargs) -> QuerySet`:  
    Returns the queryset for the admin view, optimized with `select_related("user")` to minimize database queries when fetching related user data.  
  - `get_readonly_fields(*args, **kwargs) -> list[Any]`:  
    Makes all fields read-only in the admin interface, preventing modifications.  
  - `has_add_permission(*args, **kwargs) -> bool`:  
    Disables the ability to add new outstanding tokens through the admin panel.  
  - `has_delete_permission(*args, **kwargs) -> bool`:  
    Disables the ability to delete outstanding tokens through the admin panel.  
  - `has_change_permission(request, obj=None) -> bool`:  
    Allows read-only access (`GET`, `HEAD` requests) but prevents modification via POST or other methods.

- `BlacklistedTokenAdmin(admin.ModelAdmin)`:  
  Configures the Django admin interface for the `BlacklistedToken` model, displaying blacklisted tokens along with details of their associated outstanding tokens.  
  - `get_queryset(*args, **kwargs) -> QuerySet`: Returns an optimized queryset using `select_related("token__user")` to prefetch related token and user data.  
  - `token_jti(obj: BlacklistedToken) -> str`: Returns the JTI (unique identifier) of the associated token.  
  - `token_user(obj: BlacklistedToken) -> AuthUser`: Returns the user associated with the blacklisted token.  
  - `token_created_at(obj: BlacklistedToken) -> datetime`: Returns the creation timestamp of the associated token.  
  - `token_expires_at(obj: BlacklistedToken) -> datetime`:  Returns the expiration timestamp of the associated token.  

- `admin.site.register(OutstandingToken, OutstandingTokenAdmin)`: Registers the `OutstandingToken` model with its custom admin configuration.

- `admin.site.register(BlacklistedToken, BlacklistedTokenAdmin)`: Registers the `BlacklistedToken` model with its custom admin configuration.

`apps.py` :

- `TokenBlacklistConfig(AppConfig)`  
  Defines the Django application configuration for the **Token Blacklist** app used in `rest_framework_simplejwt`.  This configuration ensures proper initialization and labeling of the blacklist feature within Django’s project structure.

`models.py` :

- `OutstandingToken(models.Model)`: A Django model representing a JWT token that has been issued and is being tracked for potential blacklisting.

  - `Meta`: `verbose_name` and `verbose_name_plural` make the model more readable in admin pages. `abstract` dynamically disables the table if the blacklist app isn’t installed. `ordering` makes queries return tokens sorted by the user by default.

  - `__str__(self)`: Returns a human-readable string representation of the token in the format `"Token for <user> (<jti>)"`.


- `BlacklistedToken`
Represents a token that has been explicitly invalidated (revoked before its expiration).
  - `Meta`: Defines model-level options for `BlacklistedToken`, such as human-readable names and abstract status. Like in `OutstandingToken`, it controls database behavior, admin display, and ORM features.
  - `__str__`:  
    Returns a readable label

## rest_framework_simplejwt/：

`__init__.py` : sets the package version for `djangorestframework_simplejwt`.

`authentication.py` :

- `JWTAuthentication.__init__(self, *args, **kwargs)`:  
  Initializes the authentication class and sets the `user_model` to the configured Django user model.

- `JWTAuthentication.authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]`:  
  Main entry point for authenticating a request. Extracts the token from the request header, validates it, and returns the corresponding user and token.

- `JWTAuthentication.authenticate_header(self, request: Request) -> str`:  
  Returns the value for the `WWW-Authenticate` header used in 401 responses.

- `JWTAuthentication.get_header(self, request: Request) -> bytes`:  
  Extracts the raw authentication header from the request, ensuring it is in byte form.

- `JWTAuthentication.get_raw_token(self, header: bytes) -> Optional[bytes]`:  
  Extracts an unvalidated JWT from the given header. Returns `None` if the header is missing or improperly formatted. Raises `AuthenticationFailed` if the header contains too many parts.

- `JWTAuthentication.get_validated_token(self, raw_token: bytes) -> Token`:  
  Validates a raw JWT against all configured token classes and returns a validated token object. Raises `InvalidToken` if no class accepts the token.

- `JWTAuthentication.get_user(self, validated_token: Token) -> AuthUser`:  
  Retrieves the user instance associated with a validated token. Performs checks for user existence, activity status, and token revocation. Raises `AuthenticationFailed` or `InvalidToken` on failure.

- `JWTStatelessUserAuthentication.get_user(self, validated_token: Token) -> AuthUser`:  
  Returns a stateless user object (`TokenUser`) for the given validated token without performing a database lookup. Raises `InvalidToken` if the token lacks a recognizable user claim.

- `default_user_authentication_rule(user: Optional[AuthUser]) -> bool`:  
  Default rule to determine whether a user can authenticate. Returns `True` if the user exists and is active (depending on `CHECK_USER_IS_ACTIVE` setting), otherwise `False`.

`backends.py` :

- `TokenBackend.__init__(self, algorithm, signing_key=None, verifying_key="", audience=None, issuer=None, jwk_url=None, leeway=None, json_encoder=None)`:  
  Initializes a token backend for encoding and decoding JWTs. Validates the algorithm, sets signing/verifying keys, audience, issuer, leeway, optional JWK client, and JSON encoder.

- `TokenBackend.prepared_signing_key`:  
  Cached property returning the signing key, processed for use with the specified JWT algorithm.

- `TokenBackend.prepared_verifying_key`:  
  Cached property returning the verifying key, processed for use with the specified JWT algorithm.

- `TokenBackend._prepare_key(self, key: Optional[str]) -> Any`:  
  Prepares a key for use with PyJWT, supporting both modern and legacy versions. Returns the key unchanged if preparation is not needed.

- `TokenBackend._validate_algorithm(self, algorithm: str) -> None`:  
  Ensures that the provided algorithm is supported and, if it requires cryptography, that the necessary library is installed. Raises `TokenBackendError` for invalid or unsupported algorithms.

- `TokenBackend.get_leeway(self) -> timedelta`:  
  Returns the configured leeway as a `timedelta` object for token expiration verification. Raises `TokenBackendError` if the type is invalid.

- `TokenBackend.get_verifying_key(self, token: Token) -> Any`:  
  Returns the appropriate key for verifying a JWT, selecting between HS keys, JWK client keys, or the pre-configured verifying key.

- `TokenBackend.encode(self, payload: dict[str, Any]) -> str`:  
  Encodes a JWT from the provided payload dictionary, applying optional audience and issuer claims. Returns the JWT as a string, compatible with different PyJWT versions.

- `TokenBackend.decode(self, token: Token, verify: bool = True) -> dict[str, Any]`:  
  Decodes and validates a JWT, returning its payload as a dictionary. Raises `TokenBackendError` for invalid tokens or algorithms and `TokenBackendExpiredToken` if the token is expired.

`exceptions.py` :

- `TokenError(Exception)`:  
  Base exception for general token-related errors.

- `ExpiredTokenError(TokenError)`:  
  Raised when a token has expired.

- `TokenBackendError(Exception)`:  
  Base exception for errors occurring in the token backend (encoding/decoding).

- `TokenBackendExpiredToken(TokenBackendError)`:  
  Raised when a token is expired during backend validation.

- `DetailDictMixin.__init__(self, detail: Union[dict[str, Any], str, None] = None, code: Optional[str] = None) -> None`:  
  Builds a detail dictionary for the exception, combining default messages and codes with user-provided details. Used to standardize error responses for API clients.

- `AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed)`: Custom exception for authentication failures, extending Django REST Framework’s `AuthenticationFailed`. Includes structured detail dictionary via `DetailDictMixin`.

- `InvalidToken(AuthenticationFailed)`: Raised when a JWT is invalid or expired.  

`models.py` :

- `TokenUser(token)`: A dummy user class modeled after `django.contrib.auth.models.AnonymousUser`.  
  Designed for stateless authentication with JWTs in systems that share a secret key. Acts as a user object backed by a validated token rather than a database record.

  - `__init__(self, token)`: Initializes the `TokenUser` instance with a validated JWT `token`.

  - `__str__(self)`: Returns a string representation of the user, including their `id`.

  - `id`: Cached property returning the user ID from the token using the claim specified in `api_settings.USER_ID_CLAIM`.

  - `pk`: Cached property alias for `id`.

  - `username`: Cached property returning the username from the token, defaulting to an empty string if not present.

  - `is_staff`: Cached property returning the `is_staff` status from the token.

  - `is_superuser`: Cached property returning the `is_superuser` status from the token.

  - `__eq__(self, other)`: Checks equality with another `TokenUser` based on the user ID.

  - `__ne__(self, other)`: Checks inequality with another `TokenUser`.

  - `__hash__(self)`: Returns a hash based on the user ID, allowing use in sets and as dict keys.

  - `save(self)`: Raises `NotImplementedError`; `TokenUser` has no database representation.

  - `delete(self)`: Raises `NotImplementedError`; `TokenUser` has no database representation.

  - `set_password(self, raw_password)`: Raises `NotImplementedError`; `TokenUser` has no database representation.

  - `check_password(self, raw_password)`: Raises `NotImplementedError`; `TokenUser` has no database representation.

  - `groups`: Property returning an empty manager for groups, since the user has no DB representation.

  - `user_permissions`: Property returning an empty manager for permissions, since the user has no DB representation.

  - `get_group_permissions(self, obj=None)`: Returns an empty set, as this user has no groups.

  - `get_all_permissions(self, obj=None)`: Returns an empty set, as this user has no permissions.

  - `has_perm(self, perm, obj=None)`: Always returns `False`; the user has no permissions.

  - `has_perms(self, perm_list, obj=None)`: Always returns `False`; the user has no permissions.

  - `has_module_perms(self, module)`: Always returns `False`; the user has no module-level permissions.

  - `is_anonymous`: Property that always returns `False`.

  - `is_authenticated`: Property that always returns `True`.

  - `get_username(self)`: Returns the `username` of the user.

  - `__getattr__(self, attr)`: Provides access to custom claims in the token; returns `None` if the attribute is not present in the token.


`serializers.py` :

- `PasswordField(*args, **kwargs)`: A custom serializer field for handling passwords. It ensures the field is write-only and sets the input type to `password` for secure handling.


- `TokenObtainSerializer(*args, **kwargs)`: Base serializer for obtaining a token given user credentials. It handles user authentication and validates the provided username and password.

  - `validate(attrs)`: Authenticates the user with the provided credentials. If authentication fails, triggers `ON_LOGIN_FAILED` and raises `AuthenticationFailed`.
  
  - `get_token(user)`: Returns an instance of the serializer’s configured token class for the given user.

- `TokenObtainPairSerializer(TokenObtainSerializer)`: Serializer for obtaining a refresh and access token pair.

  - `validate(attrs)`: Calls the base `validate`, then generates a refresh token and corresponding access token. Optionally updates last login using `ON_LOGIN_SUCCESS`.

- `TokenObtainSlidingSerializer(TokenObtainSerializer)`: Serializer for obtaining a sliding token.

  - `validate(attrs)`: Calls the base `validate`, then generates a sliding token. Optionally updates last login using `ON_LOGIN_SUCCESS`.

- `TokenRefreshSerializer(serializers.Serializer)`: Serializer for refreshing a JWT using a refresh token.

  - `validate(attrs)`: Validates the refresh token, checks user existence and authentication rules, handles password changes, optionally rotates tokens, and returns a new access token (and refresh token if rotation is enabled).

- `TokenRefreshSlidingSerializer(serializers.Serializer)`: Serializer for refreshing sliding tokens.

  - `validate(attrs)`: Validates the sliding token, checks user existence and authentication rules, handles password changes, verifies refresh expiration, updates timestamp claims, and returns a new sliding token.

- `TokenVerifySerializer(serializers.Serializer)`: Serializer for verifying the validity of a token.

  - `validate(attrs)`: Validates the provided token, and if blacklisting is enabled, checks that the token is not blacklisted.

- `TokenBlacklistSerializer(serializers.Serializer)`: Serializer for blacklisting a refresh token.

  - `validate(attrs)`: Attempts to blacklist the provided refresh token if the token class supports blacklisting.

- `default_on_login_success(user, request)`: Default callback function executed on successful login. Updates the user's last login timestamp.

- `default_on_login_failed(credentials, request)`: Default callback function executed on failed login attempts. Does nothing by default.

`settings.py` :

- `APISettings(_APISettings)`: A subclass of DRF's `APISettings` to manage Simple JWT settings.

  - `__check_user_settings(self, user_settings)`: Checks the user-provided settings dictionary for removed/deprecated keys. Raises a `RuntimeError` if a removed setting is found, directing the user to the documentation.

- `reload_api_settings(*args, **kwargs)`: Signal handler to reload `api_settings` when Django's `setting_changed` signal indicates that `SIMPLE_JWT` settings have been updated. Ensures runtime changes to settings are applied.

`state.py`:

- `token_backend`: An instance of `TokenBackend` initialized using the configuration from `api_settings`.  
  This backend handles encoding and decoding of JWTs, including verification of signatures, audience, issuer, and custom claims.  

`tokens.py` :

- `Token`: A base class for creating, decoding, verifying, and managing JWTs.

  - `__init__(self, token=None, verify=True)`: Initializes a token instance. Can wrap an existing JWT or create a new one. Raises `TokenError` or `ExpiredTokenError` if the token is invalid or expired.

  - `__repr__(self)`: Returns the `repr` of the token payload.

  - `__getitem__(self, key)`, `__setitem__(self, key, value)`, `__delitem__(self, key)`, `__contains__(self, key)`: Provide dict-like access to the token payload.

  - `get(self, key, default=None)`: Returns a claim value or a default if not present.

  - `__str__(self)`: Encodes the token payload and returns it as a signed JWT string.

  - `verify(self)`: Performs additional validation, including expiration check and token type verification.

  - `verify_token_type(self)`: Checks that the token type claim matches the expected type.

  - `set_jti(self)`: Populates the token's JTI claim with a unique identifier.

  - `set_exp(self, claim="exp", from_time=None, lifetime=None)`: Sets or updates the token's expiration claim.

  - `set_iat(self, claim="iat", at_time=None)`: Sets or updates the token's issued-at claim.

  - `check_exp(self, claim="exp", current_time=None)`: Validates that the token has not expired based on the specified claim.

  - `outstand(self)`: Ensures the token is registered in the outstanding token list. Default implementation returns `None`.

  - `for_user(cls, user)`: Class method that generates a token for a given user, including user ID and optional password hash for revocation checking.

  - `token_backend`: Property that returns the configured `TokenBackend` instance.

  - `get_token_backend(self)`: Returns the `TokenBackend` instance (backward compatibility).

- `BlacklistMixin(Generic[T])`: Mixin to add blacklist functionality for tokens if the `token_blacklist` app is installed.

  - `verify(self, *args, **kwargs)`: Extends `Token.verify` to include blacklist checking.

  - `check_blacklist(self)`: Raises `TokenError` if the token is in the blacklist.

  - `blacklist(self)`: Adds the token to the blacklist and outstanding token list.

  - `outstand(self)`: Ensures the token is present in the outstanding token list.

  - `for_user(cls, user)`: Adds the token to the outstanding token list when generating it for a user.

- `SlidingToken(BlacklistMixin["SlidingToken"], Token)`: Represents a sliding JWT token with refresh capabilities.

  - `__init__(self, *args, **kwargs)`: Initializes the token and sets the sliding refresh expiration claim for new tokens.

- `AccessToken(Token)`: Represents a standard access token.

- `RefreshToken(BlacklistMixin["RefreshToken"], Token)`: Represents a refresh token capable of generating access tokens.

  - `access_token(self)`: Property that generates an `AccessToken` from this refresh token, copying all claims except those listed in `no_copy_claims`.

- `UntypedToken(Token)`: Represents a general-purpose token that does not enforce token type verification.

  - `verify_token_type(self)`: Overrides base method; does nothing, allowing general token validation without type checks.

`utils.py` :

- `get_md5_hash_password(password)`: Returns the MD5 hash of the given password string in uppercase. Used for token revocation checks.

- `make_utc(dt)`: Ensures that a `datetime` object is timezone-aware in UTC if `USE_TZ` is enabled. Returns the original datetime if already aware or if timezone support is disabled.

- `aware_utcnow()`: Returns the current UTC datetime. Respects `USE_TZ` and returns a naive datetime if timezone support is disabled.

- `datetime_to_epoch(dt)`: Converts a `datetime` object to a Unix epoch timestamp (integer seconds since 1970-01-01 UTC).

- `datetime_from_epoch(ts)`: Converts a Unix epoch timestamp to a `datetime` object. The result is timezone-aware in UTC if `USE_TZ` is enabled; otherwise, naive.

- `format_lazy(s, *args, **kwargs)`: Lazily formats a string with the given arguments. Useful for translating and formatting messages in a deferred manner.

`views.py` :

- `TokenViewBase(generics.GenericAPIView)`: Base view for all token-related endpoints. Disables authentication and permission classes by default.  

  - `get_serializer_class(self)`: Returns the serializer class to use. Prioritizes `serializer_class` if set; otherwise imports the class from `_serializer_class`. Raises `ImportError` if the import fails.

  - `get_authenticate_header(self, request)`: Returns the `WWW-Authenticate` header string for failed authentication responses.

  - `post(self, request, *args, **kwargs)`: Handles POST requests. Validates the serializer and returns a JSON response with the validated data. Raises `InvalidToken` if validation fails due to token errors.

- `TokenObtainPairView(TokenViewBase)`: Takes user credentials and returns a pair of access and refresh tokens.  

- `TokenRefreshView(TokenViewBase)`: Takes a refresh token and returns a new access token if valid.  

- `TokenObtainSlidingView(TokenViewBase)`: Takes user credentials and returns a sliding token.  

- `TokenRefreshSlidingView(TokenViewBase)`: Refreshes a sliding token if its refresh period has not expired.  

- `TokenVerifyView(TokenViewBase)`: Validates a token without providing information about its intended use.  

- `TokenBlacklistView(TokenViewBase)`: Blacklists a token. Requires the `token_blacklist` app to be installed.  
