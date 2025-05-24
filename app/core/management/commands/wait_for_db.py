# VID: 43-40
# So because of this database or because of this directory structure, Django will automatically detect
# this as a management command.
# They will then allow us to run using Python managed API.
# django commands wait for db to be avalible
from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils  import OperationalError

class Command(BaseCommand):
    # django command wait for db
    def handle(self, *args, **options):
        #   Entry print for commands 
        self.stdout.write('waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database Unavailable, waiting 1 second.....")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
          