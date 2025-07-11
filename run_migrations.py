import os
import sys
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TEAFARM01BACKEND.settings')
django.setup()

try:
    print('Running makemigrations...')
    call_command('makemigrations')
    print('Running migrate...')
    call_command('migrate')
    print('✅ Migrations applied successfully.')
except Exception as e:
    print(f'❌ Migration error: {e}')
    sys.exit(1) 