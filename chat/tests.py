"""Test suite for chat features."""
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from .models import ChatMessage, DirectMessage


class ChatTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('alice', password='pw')
        self.u2 = User.objects.create_user('bob', password='pw')

    def test_direct_message_prune(self):
        dm = DirectMessage.objects.create(sender=self.u1, recipient=self.u2, content='hi')
        DirectMessage.objects.filter(id=dm.id).update(created_at=timezone.now() - timedelta(days=3))
        DirectMessage.prune_old()
        self.assertFalse(DirectMessage.objects.filter(id=dm.id).exists())

    def test_search_chat_messages(self):
        ChatMessage.objects.create(user=self.u1, content='hello world')
        ChatMessage.objects.create(user=self.u2, content='another')
        self.client.login(username='alice', password='pw')
        response = self.client.get(reverse('chat:index'), {'q': 'hello'})
        self.assertContains(response, 'hello world')
        self.assertNotContains(response, 'another')

    def test_profile_created(self):
        self.assertTrue(hasattr(self.u1, 'profile'))
