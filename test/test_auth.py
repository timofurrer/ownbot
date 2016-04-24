# -*- coding: utf-8 -*-
"""
    Provides a unit test class for the ownbot.auth module.
"""
from unittest import TestCase
from mock import patch, Mock

from telegram import Bot, Update

from ownbot.auth import requires_usergroup, assign_first_to

class TestAuth(TestCase):  # pylint: disable=too-many-public-methods
    """
        Provides unit tests for the ownbot.auth module.
    """

    def test_requires_usergroup_no_acc(self):
        """
            Test requires usergroup decorator if the user has no access
        """
        with patch("ownbot.user.User") as user_mock,\
                patch("test_auth.Update") as update_mock:
            user_mock = user_mock.return_value
            user_mock.has_acces.return_value = False

            @requires_usergroup("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)
                return True

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            called = my_command_handler(bot_mock, update_mock)

            self.assertIsNone(called)

    def test_requires_usergroup_acc(self):
        """
            Test requires usergroup decorator if the user has access
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:
            user_mock = user_mock.return_value
            user_mock.has_acces.return_value = True

            @requires_usergroup("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)
                return True

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            called = my_command_handler(bot_mock, update_mock)

            self.assertTrue(called)

    def test_assign_first_to(self):
        """
            Test assign first to decorator.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:

            user_mock = user_mock.return_value
            user_mock.group_empty.return_value = True

            @assign_first_to("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(bot_mock, update_mock)

            self.assertTrue(user_mock.save.called)

    def test_assign_first_to_not_first(self):
        """
            Test assign first to decorator if the users is not first.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:

            user_mock = user_mock.return_value
            user_mock.group_empty.return_value = False

            @assign_first_to("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(bot_mock, update_mock)

            self.assertFalse(user_mock.save.called)

    def test_assign_first_to_with_self(self):
        """
            Test assign first to decorator with self as first argument.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:

            user_mock = user_mock.return_value
            user_mock.group_empty.return_value = True

            @assign_first_to("foo")
            def my_command_handler(self, bot, update):
                """Dummy command handler"""
                print(self, bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(None, bot_mock, update_mock)

            self.assertTrue(user_mock.save.called)
