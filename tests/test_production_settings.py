import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured
from skybook import settings as project_settings

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_ENVIRONMENT_KEYS = {
    "ALLOWED_HOSTS",
    "CSRF_TRUSTED_ORIGINS",
    "DATABASE_URL",
    "DEBUG",
    "DJANGO_DB_PATH",
    "RENDER",
    "RENDER_EXTERNAL_HOSTNAME",
    "SECURE_HSTS_SECONDS",
    "SECRET_KEY",
}

SETTINGS_SNAPSHOT = """
import json
from skybook import settings

print(json.dumps({
    "allowed_hosts": settings.ALLOWED_HOSTS,
    "csrf_trusted_origins": settings.CSRF_TRUSTED_ORIGINS,
    "csrf_cookie_secure": getattr(settings, "CSRF_COOKIE_SECURE", False),
    "database_engine": settings.DATABASES["default"]["ENGINE"],
    "database_host": settings.DATABASES["default"].get("HOST", ""),
    "database_name": str(settings.DATABASES["default"]["NAME"]),
    "debug": settings.DEBUG,
    "middleware": settings.MIDDLEWARE,
    "secret_key": settings.SECRET_KEY,
    "secure_proxy_ssl_header": getattr(settings, "SECURE_PROXY_SSL_HEADER", None),
    "secure_hsts_seconds": getattr(settings, "SECURE_HSTS_SECONDS", 0),
    "secure_ssl_redirect": getattr(settings, "SECURE_SSL_REDIRECT", False),
    "session_cookie_secure": getattr(settings, "SESSION_COOKIE_SECURE", False),
    "static_backend": settings.STORAGES["staticfiles"]["BACKEND"],
    "static_root": str(settings.STATIC_ROOT),
    "static_url": settings.STATIC_URL,
}))
"""


def run_settings_snapshot(**environment_overrides):
    environment = os.environ.copy()
    for key in SETTINGS_ENVIRONMENT_KEYS:
        environment.pop(key, None)
    environment.update(environment_overrides)

    result = subprocess.run(
        [sys.executable, "-c", SETTINGS_SNAPSHOT],
        cwd=PROJECT_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_environment_helpers_parse_valid_values(monkeypatch):
    monkeypatch.setenv("TEST_BOOLEAN", "ON")
    monkeypatch.setenv("TEST_LIST", "first, second, ,")
    monkeypatch.setenv("TEST_INTEGER", "7200")

    assert project_settings.environment_bool("TEST_BOOLEAN") is True
    assert project_settings.environment_list("TEST_LIST") == ["first", "second"]
    assert project_settings.environment_int("TEST_INTEGER", default=1) == 7200

    monkeypatch.setenv("TEST_BOOLEAN", "off")
    assert project_settings.environment_bool("TEST_BOOLEAN") is False


@pytest.mark.parametrize("value", ["unknown", ""])
def test_environment_bool_rejects_invalid_values(monkeypatch, value):
    monkeypatch.setenv("TEST_BOOLEAN", value)

    with pytest.raises(ImproperlyConfigured, match="TEST_BOOLEAN must be a boolean value"):
        project_settings.environment_bool("TEST_BOOLEAN")


@pytest.mark.parametrize("value", ["unknown", "-1"])
def test_environment_int_rejects_invalid_values(monkeypatch, value):
    monkeypatch.setenv("TEST_INTEGER", value)

    with pytest.raises(
        ImproperlyConfigured,
        match="TEST_INTEGER must be a non-negative integer",
    ):
        project_settings.environment_int("TEST_INTEGER", default=1)


def test_environment_helpers_use_defaults(monkeypatch):
    monkeypatch.delenv("TEST_BOOLEAN", raising=False)
    monkeypatch.delenv("TEST_LIST", raising=False)
    monkeypatch.delenv("TEST_INTEGER", raising=False)

    assert project_settings.environment_bool("TEST_BOOLEAN", default=True) is True
    assert project_settings.environment_list("TEST_LIST", default=("local",)) == ["local"]
    assert project_settings.environment_int("TEST_INTEGER", default=3600) == 3600


def test_render_settings_branches_load_in_process(monkeypatch):
    with monkeypatch.context() as render_environment:
        for key in SETTINGS_ENVIRONMENT_KEYS:
            render_environment.delenv(key, raising=False)
        render_environment.setenv("RENDER", "true")
        render_environment.setenv("SECRET_KEY", "test-secret")
        render_environment.setenv("RENDER_EXTERNAL_HOSTNAME", "skybook.onrender.com")
        render_environment.setenv(
            "DATABASE_URL",
            "postgresql://skybook:password@postgres.internal:5432/skybook",
        )

        render_settings = importlib.reload(project_settings)

        assert render_settings.IS_RENDER is True
        assert render_settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
        assert render_settings.SECURE_HSTS_SECONDS == 3600

    importlib.reload(project_settings)


def test_local_settings_use_safe_and_convenient_defaults():
    snapshot = run_settings_snapshot()

    assert snapshot["debug"] is False
    assert snapshot["secret_key"] == "django-insecure-skybook-development-only"
    assert snapshot["allowed_hosts"] == ["localhost", "127.0.0.1", "[::1]"]
    assert snapshot["csrf_trusted_origins"] == [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    assert snapshot["database_engine"] == "django.db.backends.sqlite3"
    assert snapshot["database_name"].endswith("db.sqlite3")
    assert snapshot["static_backend"].endswith("StaticFilesStorage")


def test_local_environment_values_override_defaults():
    snapshot = run_settings_snapshot(
        DEBUG="yes",
        SECRET_KEY="local-test-secret",
        ALLOWED_HOSTS="localhost, testserver, ",
        CSRF_TRUSTED_ORIGINS="http://localhost:8000, https://example.test",
    )

    assert snapshot["debug"] is True
    assert snapshot["secret_key"] == "local-test-secret"
    assert snapshot["allowed_hosts"] == ["localhost", "testserver"]
    assert snapshot["csrf_trusted_origins"] == [
        "http://localhost:8000",
        "https://example.test",
    ]


def test_invalid_boolean_environment_value_fails_configuration():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(DEBUG="sometimes")

    assert "DEBUG must be a boolean value" in error.value.stderr


def test_render_requires_secret_key():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(RENDER="true")

    assert "SECRET_KEY is required when running on Render" in error.value.stderr


def test_render_requires_hostname_or_explicit_allowed_hosts():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(RENDER="true", SECRET_KEY="test-secret")

    assert (
        "RENDER_EXTERNAL_HOSTNAME or a non-empty ALLOWED_HOSTS value is required"
        in error.value.stderr
    )


def test_render_rejects_explicitly_empty_allowed_hosts():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(
            RENDER="true",
            SECRET_KEY="test-secret",
            RENDER_EXTERNAL_HOSTNAME="skybook.onrender.com",
            ALLOWED_HOSTS=" , ",
        )

    assert "a non-empty ALLOWED_HOSTS value is required" in error.value.stderr


def test_render_requires_trusted_origin_without_render_hostname():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(
            RENDER="true",
            SECRET_KEY="test-secret",
            ALLOWED_HOSTS="custom.example.com",
        )

    assert "A non-empty CSRF_TRUSTED_ORIGINS value is required" in error.value.stderr


def test_render_rejects_explicitly_empty_trusted_origins():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(
            RENDER="true",
            SECRET_KEY="test-secret",
            RENDER_EXTERNAL_HOSTNAME="skybook.onrender.com",
            CSRF_TRUSTED_ORIGINS=" , ",
        )

    assert "A non-empty CSRF_TRUSTED_ORIGINS value is required" in error.value.stderr


def test_render_accepts_explicit_host_and_trusted_origin_without_render_hostname():
    snapshot = run_settings_snapshot(
        RENDER="true",
        SECRET_KEY="test-secret",
        ALLOWED_HOSTS="custom.example.com",
        CSRF_TRUSTED_ORIGINS="https://custom.example.com",
    )

    assert snapshot["allowed_hosts"] == ["custom.example.com"]
    assert snapshot["csrf_trusted_origins"] == ["https://custom.example.com"]


def test_render_rejects_debug_mode():
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_settings_snapshot(RENDER="true", DEBUG="true", SECRET_KEY="test-secret")

    assert "DEBUG must be false when running on Render" in error.value.stderr


def test_render_uses_postgresql_static_and_https_settings():
    snapshot = run_settings_snapshot(
        RENDER="true",
        SECRET_KEY="test-secret",
        DATABASE_URL="postgresql://skybook:password@postgres.internal:5432/skybook",
        RENDER_EXTERNAL_HOSTNAME="skybook.onrender.com",
    )

    assert snapshot["debug"] is False
    assert snapshot["database_engine"] == "django.db.backends.postgresql"
    assert snapshot["database_host"] == "postgres.internal"
    assert snapshot["database_name"] == "skybook"
    assert snapshot["allowed_hosts"] == ["skybook.onrender.com"]
    assert snapshot["csrf_trusted_origins"] == ["https://skybook.onrender.com"]
    assert snapshot["static_backend"] == ("whitenoise.storage.CompressedManifestStaticFilesStorage")
    assert snapshot["secure_proxy_ssl_header"] == ["HTTP_X_FORWARDED_PROTO", "https"]
    assert snapshot["secure_hsts_seconds"] == 3600
    assert snapshot["secure_ssl_redirect"] is True
    assert snapshot["session_cookie_secure"] is True
    assert snapshot["csrf_cookie_secure"] is True


def test_render_hsts_duration_is_configurable():
    snapshot = run_settings_snapshot(
        RENDER="true",
        SECRET_KEY="test-secret",
        RENDER_EXTERNAL_HOSTNAME="skybook.onrender.com",
        SECURE_HSTS_SECONDS="7200",
    )

    assert snapshot["secure_hsts_seconds"] == 7200


def test_whitenoise_follows_security_middleware_and_static_paths_are_defined():
    snapshot = run_settings_snapshot()
    middleware = snapshot["middleware"]

    security_index = middleware.index("django.middleware.security.SecurityMiddleware")
    assert middleware[security_index + 1] == "whitenoise.middleware.WhiteNoiseMiddleware"
    assert snapshot["static_url"] == "/static/"
    assert snapshot["static_root"].endswith("staticfiles")


def test_render_blueprint_defines_the_production_lifecycle():
    blueprint = (PROJECT_ROOT / "render.yaml").read_text()

    assert "runtime: python" in blueprint
    assert "plan: free" in blueprint
    assert "branch: main" in blueprint
    assert "autoDeployTrigger: checksPass" in blueprint
    assert (
        "buildCommand: uv sync --frozen --no-dev"
        " && uv run python manage.py migrate"
        " && uv run python manage.py collectstatic --noinput"
    ) in blueprint
    assert "preDeployCommand" not in blueprint
    assert (
        "startCommand: uv run gunicorn skybook.wsgi:application --bind 0.0.0.0:$PORT"
    ) in blueprint
    assert "healthCheckPath: /health/" in blueprint
    assert "generateValue: true" in blueprint
    assert "property: connectionString" in blueprint
    assert "name: skybook-postgres" in blueprint
    assert "key: PYTHON_VERSION" in blueprint
    assert "value: 3.12.8" in blueprint
