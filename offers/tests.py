"""Tests for the offers app."""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Offer
from chat.models import ChatMessage


class OfferTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pw')
        self.user.profile.is_approved = True
        self.user.profile.save()

    def test_create_and_share_offer(self):
        self.client.login(username='alice', password='pw')
        response = self.client.post(reverse('offers:create'), {
            'title': 'Grocery help',
            'description': 'I can buy groceries',
            'category': 'shopping',
            'latitude': 50,
            'longitude': 10,
        })
        offer = Offer.objects.get(title='Grocery help')
        self.assertRedirects(response, reverse('offers:detail', args=[offer.id]))
        share_url = reverse('offers:share', args=[offer.id])
        self.client.get(share_url)
        self.assertTrue(ChatMessage.objects.filter(offer=offer).exists())
