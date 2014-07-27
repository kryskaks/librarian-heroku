from app import app
from app.views import index
import os
import shell

print 'Started database initialization'
shell.init_db()
print 'Tables are created'
print 'Started data import'
shell.fill_data()
print 'Database is successfully initialized'

print 'App is started'