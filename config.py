import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

DEBUG_TB_INTERCEPT_REDIRECTS = False

ADMINS = frozenset(['kryskaks@gmail.com'])

SECRET_KEY = '\xc9zW\xfd\xd5\r`\xf4aU\x8fP\x10\xc7\x8fp\xa7\xbdI|TK-\xd2'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_PATH = os.path.join(_basedir, 'app.db')

DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True

CSRF_SESSION_KEY = ""

USERS = {
	"admin" : "adminp@ss",
	"user" : "userp@ss"	
}