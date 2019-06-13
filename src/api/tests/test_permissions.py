from django.test import TestCase, RequestFactory
from django.urls import reverse
from mock import MagicMock
from api import permissions


class PermissionsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = MagicMock()
        self.permission = permissions.GetAndPostOnly()

    def test_success_get_and_post_only(self):
        request = self.factory.get(reverse('callrecord-list'))
        self.assertTrue(self.permission.has_permission(request, self.view))

        request = self.factory.post(reverse('callrecord-list'))
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_fail_get_and_post_only(self):
        request = self.factory.put(reverse('callrecord-list'))
        self.assertFalse(self.permission.has_permission(request, self.view))

        request = self.factory.delete(reverse('callrecord-list'))
        self.assertFalse(self.permission.has_permission(request, self.view))

        request = self.factory.head(reverse('callrecord-list'))
        self.assertFalse(self.permission.has_permission(request, self.view))

        request = self.factory.options(reverse('callrecord-list'))
        self.assertFalse(self.permission.has_permission(request, self.view))

        request = self.factory.trace(reverse('callrecord-list'))
        self.assertFalse(self.permission.has_permission(request, self.view))
