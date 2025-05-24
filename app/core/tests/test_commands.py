# test custome management command
from unittest.mock import patch, call #We're going to mock the behavior of the database because we need to be able to simulate when the database
from psycopg2 import OperationalError as psycopg2Error #It's one of the possibilities of the errors that we might get when we try and connect to the database
# before the database is ready.
from django.core.management import call_command #this allows us to actually call the command that we're testing.
from django.db.utils import OperationalError #And then we have another operational error, which is another exception that may get thrown by the database
# depending on what stage of the start up process it is.
from django.test import SimpleTestCase #And then we have a simple test case, which is the base test course that we're going to use for testing
# out our unit test or creating our unit test.

@patch("core.management.commands.wait_for_db.Command.check") #So this is basically the command that we're going to be mocking.
class CommandTests(SimpleTestCase):
    # Test commands
    def test_wait_for_db_ready(self, patched_check):
        # Test waiting for db if db is ready
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=['default'])
    @patch('time.sleep')
    def test_wait_for_db_delay(self,patched_sleep, patched_check):
        # Test waiting db when getting OperationalError
        patched_check.side_effect = [psycopg2Error] * 2 + \
        [OperationalError] * 3 + [True] #[\]And then this is just the syntax to break this onto a different line here.
        # So the side effect allows you to pass in various different items that get handled differently dependingon that type.
        # So if we pass in an exception, then the mocking library knows that it should raise that exception.
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


