#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the django ERP project.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014, django ERP Team'
__version__ = '0.0.5'

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import *

class NotificationQuerySetTestCase(TestCase):
    def setUp(self):
        from django.utils.timezone import make_aware, get_current_timezone
        
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username=u"u1")
        self.u2 = user_model.objects.create(username=u"u2")
        self.signature = Signature.objects.create(slug=u"object-created")
        self.read_datetime = make_aware(datetime(2014, 1, 12, 16, 27, 0), get_current_timezone())
        self.n1 = Notification.objects.create(title=u"n1", target=self.u1, signature=self.signature)
        self.n2 = Notification.objects.create(title=u"n2", target=self.u1, signature=self.signature)
        self.n3 = Notification.objects.create(title=u"n3", target=self.u2, signature=self.signature)
        self.n4 = Notification.objects.create(title=u"n4", target=self.u1, signature=self.signature, read=self.read_datetime)
        self.n5 = Notification.objects.create(title=u"n5", target=self.u2, signature=self.signature, read=self.read_datetime)
        
    def test_read(self):
        """Tests returning read notifications.
        """
        self.assertQuerysetEqual(
            Notification.objects.read(),
            [
                repr(self.n4),
                repr(self.n5),
            ],
            ordered=False
        )
        
    def test_unread(self):
        """Tests returning unread notifications.
        """
        self.assertQuerysetEqual(
            Notification.objects.unread(),
            [
                repr(self.n1),
                repr(self.n2),
                repr(self.n3),
            ],
            ordered=False
        )
        
    def test_for_object(self):
        """Tests returning notifications for a given object.
        """
        self.assertQuerysetEqual(
            Notification.objects.for_object(self.u1),
            [
                repr(self.n1),
                repr(self.n2),
                repr(self.n4),
            ],
            ordered=False
        )
        
    def test_read_for_object(self):
        """Tests returning read notifications for a given object.
        """
        self.assertQuerysetEqual(
            Notification.objects.read_for_object(self.u1),
            [
                repr(self.n4),
            ],
            ordered=False
        )
        
    def test_unread_for_object(self):
        """Tests returning unread notifications for a given object.
        """
        self.assertQuerysetEqual(
            Notification.objects.unread_for_object(self.u1),
            [
                repr(self.n1),
                repr(self.n2),
            ],
            ordered=False
        )
