"""
Production settings for config project.

These settings extend the base settings.py and override
values for production deployment.

Usage:
    Set DJANGO_SETTINGS_MODULE=config.settings_production

Required environment variables:
    - DJANGO_SECRET_KEY: Secret key for cryptographic signing
    - DJANGO_ALLOWED_HOSTS: Comma-separated list of allowed hosts

Optional environment variables:
    - DJANGO_USE_HTTPS: Set to 'true' to enable HTTPS security settings
"""

import os
from .settings import *  # noqa: F401, F403

# Production flag - always False in production
DEBUG = False

# Allowed hosts must be explicitly set in production via environment
ALLOWED_HOSTS_ENV = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]
else:
    # In production, require explicit host configuration
    raise ValueError(
        "DJANGO_ALLOWED_HOSTS environment variable is required in production. "
        "Set it to your domain(s), e.g., 'smaki-lodow.pl,www.smaki-lodow.pl'"
    )

# Secret key must be set via environment in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is required in production. "
        "Generate one with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
    )

# HTTPS Security Settings
# These require HTTPS to be enabled on your deployment platform
USE_HTTPS = os.environ.get('DJANGO_USE_HTTPS', 'true').lower() in ('true', '1', 'yes')

if USE_HTTPS:
    # Redirect all HTTP to HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # HSTS (HTTP Strict Transport Security)
    # Forces browsers to use HTTPS for 1 year (in seconds)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDEMANS = True
    SECURE_HSTS_PRELOAD = True

    # Secure cookies - only sent over HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filter (limited browser support)
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking via iframe embedding

# Additional security settings
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Performance and caching
# WhiteNoise already handles static file compression and caching headers
# No additional configuration needed - CompressedManifestStaticFilesStorage
# is already set in base settings

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
