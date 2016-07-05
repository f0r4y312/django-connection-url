# -*- coding: utf-8 -*-

import os
from uuid import uuid4

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass


DB_SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'mysql-connector': 'mysql.connector.django',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
    'oraclegis': 'django.contrib.gis.db.backends.oracle',
}

CACHE_SCHEMES = {
    'locmem': 'django.core.cache.backends.locmem.LocMemCache',
    'memcached': 'django.core.cache.backends.memcached.MemcachedCache',
    'redis': 'redis_cache.RedisCache',
}

def config(env, *args, **kwargs):
    """Returns configured dictionary object from env var."""

    config = {}

    cnxn_url = os.environ.get(env, env)

    if isinstance(cnxn_url, str):
        if cnxn_url == 'sqlite://:memory:':
            # this is a special case, because if we pass this URL into
            # urlparse, urlparse will choke trying to interpret "memory"
            # as a port number
            return {
                'ENGINE': DB_SCHEMES['sqlite'],
                'NAME': ':memory:'
            }
            # note: no other settings are required for sqlite
        # otherwise parse the url as normal

        # Register database/cache schemes in URLs.
        uses_netloc = urlparse.uses_netloc[:]
        urlparse.uses_netloc.extend(DB_SCHEMES.keys())
        urlparse.uses_netloc.extend(CACHE_SCHEMES.keys())

        # Parse connection URL.
        url = urlparse.urlparse(cnxn_url)
        # Split query strings from path.
        path = url.path[1:]
        if '?' in path and not url.query:
            path, query = path.split('?', 2)
        else:
            path, query = path, url.query
        query = urlparse.parse_qs(query)

        # Unregister database/cache schemes in URLs.
        urlparse.uses_netloc = uses_netloc

        # Update with environment configuration.
        if url.scheme in DB_SCHEMES:
            config = config_db(url, path)
        elif url.scheme in CACHE_SCHEMES:
            config = config_cache(url, path)
        else:
            raise ImproperlyConfigured(
                    "Cannot resolve connection URL scheme '%s' in %s (%s) into engine. Choices are: %s" %
                    (url.scheme, env, cnxn_url, ', '.join(sorted(DB_SCHEMES.keys()) + sorted(CACHE_SCHEMES.keys()))))

        # Pass the query string into OPTIONS.
        options = {}
        for key, values in query.items():
            options[key] = values[-1]

        if options:
            # Support for Postgres Schema URLs
            if 'currentSchema' in options and config['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
                options['options'] = '-c search_path={0}'.format(options['currentSchema'])
            config['OPTIONS'] = options

    # Use dict args to set default values if not already set
    for arg in args:
        if isinstance(arg, dict):
            default = arg.copy()
            default_options = arg.pop('OPTIONS', {}).copy()
            default_options.update(config.pop('OPTIONS', {}))
            default.update(config)
            if default_options:
                default['OPTIONS'] = default_options
            config = default

    # Use kwargs to override any parsed values
    for cfg,val in kwargs.items():
        config[cfg] = val

    return config


def config_db(url, path):
    """Parses a database URL."""

    config = {}

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Update with environment configuration.
    config.update({
        'ENGINE': DB_SCHEMES.get(url.scheme, ''),
        'NAME': urlparse.unquote(path or ''),
        'USER': urlparse.unquote(url.username or ''),
        'PASSWORD': urlparse.unquote(url.password or ''),
        'HOST': (url.hostname or '').replace('%2f', '/').replace('%2F', '/'),
        'PORT': url.port or '',
    })

    return config


def config_cache(url, path):
    """Parses a cache URL."""

    config = {}

    # if we are using locmem and we have no hostname,
    # then assume we want a random unique id
    if url.scheme == 'locmem' and not path:
        path = uuid4().hex
    else:
        path = '%(host)s%(port)s%(path)s' % {
            'host': url.hostname,
            'port': (':%s' % url.port) if url.port else '',
            'path': (':%s' % url.path) if url.path else '',
        }

    # Update with environment configuration.
    config.update({
        'BACKEND': CACHE_SCHEMES.get(url.scheme, ''),
        'LOCATION': path
    })
    if url.password:
        config.update({
            'OPTIONS': {
                'PASSWORD': url.password,
            }
        })

    return config
