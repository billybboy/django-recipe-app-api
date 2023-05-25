"""
Test custom Django management command.
"""
# mock the bahavior of the database
from unittest.mock import patch

# Error we might get when trying to connect the database before it is ready
from psycopg2 import OperationalError as Psycopg2Error

# call_command is a helper function that allows us to call
# the command by the name
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# the command to be mocking
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # testing what happens or what should happen when the database is not ready
    # database return some exceptions or the check method returns some
    # exceptions indicate the database isn't ready
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
