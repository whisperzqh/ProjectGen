# PRD Document for djangorestframework-simplejwt

## Introduction

The purpose of this project is to develop a JSON Web Token (JWT) authentication plugin for Django REST Framework .The repository provides a complete, production-ready implementation of JWT-based authentication with support for token generation, validation, refresh, and revocation. This library is designed for developers building REST APIs with Django who need stateless, token-based authentication.

## Goals

The objective of this project is to provide a robust, secure JWT authentication system for Django REST Framework that handles the complete token lifecycle including generation, validation, refresh, and blacklisting. The library should support both stateless and database-backed authentication modes, offer extensive customization options, and follow JWT specifications (RFC 7519) while maintaining secure defaults.

## Features and Functionalities

The following features and functionalities are expected in the project:

### Token Generation and Authentication
- Ability to generate JWT access/refresh token pairs for authenticated users
- Ability to generate sliding tokens that combine access and refresh functionality
- Ability to authenticate API requests using JWT tokens from Authorization headers
- Ability to validate token signatures, expiration, and claims
- Ability to operate in stateless mode without database lookups using `JWTStatelessUserAuthentication`

### Token Lifecycle Management
- Ability to refresh access tokens using refresh tokens without re-authentication
- Ability to verify HMAC-signed tokens without access to signing keys
- Ability to blacklist tokens before their natural expiration
- Ability to track all outstanding tokens in the database
- Ability to rotate refresh tokens on each use for enhanced security

### Cryptographic Support
- Ability to use HMAC algorithms (HS256, HS384, HS512) for token signing
- Ability to use RSA algorithms (RS256, RS384, RS512) with public/private key pairs
- Ability to use ECDSA algorithms (ES256, ES384, ES512) with elliptic curve keys
- Ability to configure custom signing and verifying keys
- Ability to support JWK (JSON Web Key) URLs for key distribution

### Token Blacklisting
- Ability to add tokens to a blacklist database
- Ability to blacklist tokens programmatically using the `blacklist()` method 
- Ability to blacklist tokens via API endpoint
- Ability to flush expired tokens from the database using management command

### Customization and Extension
- Ability to customize token lifetimes for access and refresh tokens
- Ability to customize token claims and payload content
- Ability to extend serializers for custom validation logic
- Ability to override authentication rules and user lookup behavior
- Ability to create custom token classes by inheriting from base `Token` class

### Internationalization
- Ability to display error messages in multiple languages 
- Ability to contribute translations via pull requests or inlang platform 

## Technical Constraints

- The repository should use Python (3.8-3.11) as the primary programming language
- The repository should be compatible with Django (3.2-4.2)
- The repository should integrate with Django REST Framework (3.10-3.14)
- The repository should use PyJWT library for JWT encoding/decoding operations
- The repository should follow JWT specifications as defined in RFC 7519

## Requirements

### Dependencies

- `Django>=3.2,<5.0` - Web framework
- `djangorestframework>=3.10,<4.0` - REST API framework
- `PyJWT>=1.7.1,<3.0` - JWT encoding and decoding library

### Optional Dependencies

- `cryptography` - Required for RSA and ECDSA digital signature algorithms

### Development Dependencies

- Testing frameworks and tools for quality assurance

## Usage

### Installation

Install Simple JWT with pip:

```bash
pip install djangorestframework-simplejwt
```

For cryptographic algorithm support:

```bash
pip install djangorestframework-simplejwt[crypto]
```

### Basic Configuration

Add JWT authentication to Django settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

Configure URL routes for token endpoints: 

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Token Blacklist Setup

Enable token blacklisting by adding the app to installed apps:

```python
INSTALLED_APPS = (
    'rest_framework_simplejwt.token_blacklist',
)
```

Run migrations:

```bash
python manage.py migrate
```

Add blacklist endpoint to URLs:

```python
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
```

### Advanced Usage Examples

Blacklist a token programmatically: 

```python
from rest_framework_simplejwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

Blacklist via API:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}' \
  http://localhost:8000/api/token/blacklist/
```

## API Endpoints

### Token Obtain Pair
- **Endpoint**: `/api/token/`
- **Method**: POST
- **Purpose**: Obtain access and refresh token pair using username/password
- **View**: `TokenObtainPairView`
- **Serializer**: `TokenObtainPairSerializer`

### Token Refresh
- **Endpoint**: `/api/token/refresh/`
- **Method**: POST
- **Purpose**: Obtain new access token using refresh token
- **View**: `TokenRefreshView`
- **Serializer**: `TokenRefreshSerializer`

### Token Verify
- **Endpoint**: `/api/token/verify/`
- **Method**: POST
- **Purpose**: Verify token validity without decoding 
- **View**: `TokenVerifyView`

### Token Blacklist
- **Endpoint**: `/api/token/blacklist/`
- **Method**: POST
- **Purpose**: Add refresh token to blacklist 
- **View**: `TokenBlacklistView`

## Terms/Concepts Explanation

**JWT (JSON Web Token)**: A compact, URL-safe token format for securely transmitting information between parties as a JSON object, digitally signed to verify authenticity.

**Access Token**: Short-lived JWT token used to authenticate API requests, typically expires in 5 minutes.

**Refresh Token**: Longer-lived JWT token used to obtain new access tokens without re-authentication, typically expires in 1 day.

**Sliding Token**: A token type that combines access and refresh functionality, can be refreshed to extend its lifetime.

**Token Blacklist**: A database-backed system for revoking tokens before their natural expiration by marking them as invalid. 

**Stateless Authentication**: Authentication mode where user information is derived entirely from token claims without database lookups, enabled via `JWTStatelessUserAuthentication`.

**Outstanding Token**: A database record tracking all issued refresh and sliding tokens for blacklist management.

**Token Backend**: Component responsible for cryptographic operations including encoding, decoding, and signature verification using PyJWT.
