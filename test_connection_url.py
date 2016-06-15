# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import connection_url


POSTGIS_URL = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'


class DatabaseTestSuite(unittest.TestCase):

    def test_postgres(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_postgres_unix_socket(self):
        url = 'postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == '/var/run/postgresql'
        assert url['USER'] == ''
        assert url['PASSWORD'] == ''
        assert url['PORT'] == ''

    def test_postgres_search_path(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema'
        url = connection_url.config(url)
        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431
        assert url['OPTIONS']['options'] == '-c search_path=otherschema'


    def test_postgres_with_special_characters(self):
        url = 'postgres://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == '#database'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == '#user'
        assert url['PASSWORD'] == '#password'
        assert url['PORT'] == 5431

    def test_postgis(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.postgis'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_gis(self):
        url = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.mysql'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_connector(self):
        url = 'mysql-connector://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'mysql.connector.django'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_oracle(self):
        url = 'oracle://scott:tiger@oraclehost:1521/hr'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['NAME'] == 'hr'
        assert url['HOST'] == 'oraclehost'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['PORT'] == 1521

    def test_oracle_gis(self):
        url = 'oraclegis://scott:tiger@oraclehost:1521/hr'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.oracle'
        assert url['NAME'] == 'hr'
        assert url['HOST'] == 'oraclehost'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['PORT'] == 1521

    def test_oracle_dsn(self):
        url = (
            'oracle://scott:tiger@/'
            '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
            '(HOST=oraclehost)(PORT=1521)))'
            '(CONNECT_DATA=(SID=hr)))'
        )
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['HOST'] == ''
        assert url['PORT'] == ''

        dsn = (
            '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
            '(HOST=oraclehost)(PORT=1521)))'
            '(CONNECT_DATA=(SID=hr)))'
        )

        assert url['NAME'] == dsn

    def test_oracle_tns(self):
        url = 'oracle://scott:tiger@/tnsname'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['NAME'] == 'tnsname'
        assert url['HOST'] == ''
        assert url['PORT'] == ''

    def test_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url, ENGINE=engine)

        assert url['ENGINE'] == engine

    def test_conn_max_age_setting(self):
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url, CONN_MAX_AGE=conn_max_age)

        assert url['CONN_MAX_AGE'] == conn_max_age

    def test_default_settings(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url, {'ENGINE':engine, 'CONN_MAX_AGE': conn_max_age})

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['CONN_MAX_AGE'] == conn_max_age

    def test_override_settings(self):
        engine = 'mysql.connector.django'
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url,
                {'ENGINE':'django_mysqlpool.backends.mysqlpool', 'CONN_MAX_AGE': conn_max_age},
                ENGINE=engine)

        assert url['ENGINE'] == engine
        assert url['CONN_MAX_AGE'] == conn_max_age

    def test_default_options(self):
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url, {'CONN_MAX_AGE': conn_max_age, 'OPTIONS': {'MAX_CONNECTIONS': 120, 'TIMEOUT': 100}})

        assert url['CONN_MAX_AGE'] == conn_max_age
        assert url['OPTIONS'] == {
            'reconnect': 'true',
            'MAX_CONNECTIONS': 120,
            'TIMEOUT': 100,
        }

    def test_override_options(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url, {'OPTIONS': {'MAX_CONNECTIONS': 120}}, OPTIONS={'TIMEOUT': 100})

        assert url['OPTIONS'] == {
            'TIMEOUT': 100,
        }

    def test_database_url(self):
        os.environ.pop('DATABASE_URL', None)
        self.assertRaises(connection_url.ImproperlyConfigured, connection_url.config, 'DATABASE_URL')

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        url = connection_url.config('DATABASE_URL')

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_database_url_with_options(self):
        # Test full options
        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?sslrootcert=rds-combined-ca-bundle.pem&sslmode=verify-full'
        url = connection_url.config('DATABASE_URL')

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431
        assert url['OPTIONS'] == {
            'sslrootcert': 'rds-combined-ca-bundle.pem',
            'sslmode': 'verify-full'
        }

        # Test empty options
        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?'
        url = connection_url.config('DATABASE_URL')
        assert 'OPTIONS' not in url

    def test_cleardb(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = connection_url.config(url)

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'heroku_97681db3eff7580'
        assert url['HOST'] == 'us-cdbr-east.cleardb.com'
        assert url['USER'] == 'bea6eb025ca0d8'
        assert url['PASSWORD'] == '69772142'
        assert url['PORT'] == ''


if __name__ == '__main__':
    unittest.main()
