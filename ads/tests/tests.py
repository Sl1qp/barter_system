from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, Category, Condition, ExchangeProposal

USER1_ = "barter_user"
USER2_ = "test_barter_user"
PASSWORD_ = "barter_system_0424ok"


class AdTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username=USER1_, password=PASSWORD_)
        self.user2 = User.objects.create_user(username=USER2_, password=PASSWORD_)

        self.category = Category.objects.create(name="Электроника")
        self.condition = Condition.objects.create(name="Новый")

        self.ad = Ad.objects.create(
            user=self.user1,
            title="Тестовое объявление",
            description="Описание",
            category=self.category,
            condition=self.condition,
        )

        self.client = Client()

    def test_ad_creation_authenticated(self):
        self.client.login(username=USER1_, password=PASSWORD_)
        response = self.client.post(
            reverse("ads:ad-create"),
            {
                "title": "Новое объявление",
                "description": "Описание",
                "category": self.category.id,
                "condition": self.condition.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_creation_unauthenticated(self):
        response = self.client.post(reverse("ads:ad-create"))
        self.assertEqual(response.status_code, 302)

    def test_ad_edit_by_non_owner(self):
        self.client.login(username=USER2_, password=PASSWORD_)
        response = self.client.post(reverse("ads:ad-edit", args=[self.ad.id]))
        self.assertEqual(response.status_code, 403)

    def test_ad_delete_by_owner(self):
        self.client.login(username=USER1_, password=PASSWORD_)
        response = self.client.post(reverse("ads:ad-delete", args=[self.ad.id]))
        self.assertEqual(Ad.objects.count(), 0)

    def test_ad_delete_by_non_owner(self):
        self.client.login(username=USER2_, password=PASSWORD_)
        response = self.client.post(reverse("ads:ad-delete", args=[self.ad.id]))
        self.assertEqual(response.status_code, 403)


class ProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username=USER1_, password=PASSWORD_)
        self.user2 = User.objects.create_user(username=USER2_, password=PASSWORD_)
        self.ad1 = Ad.objects.create(user=self.user1, title="Ad1")
        self.ad2 = Ad.objects.create(user=self.user2, title="Ad2")

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Предложение обмена",
        )

    def test_proposal_creation(self):
        self.client.login(username=USER1_, password=PASSWORD_)
        response = self.client.post(
            reverse("ads:proposal-create"),
            {
                "ad_sender": self.ad1.id,
                "ad_receiver": self.ad2.id,
                "comment": "Новое предложение",
            },
        )
        self.assertEqual(ExchangeProposal.objects.count(), 2)

    def test_proposal_status_update_by_receiver(self):
        self.client.login(username=USER2_, password=PASSWORD_)
        response = self.client.post(
            reverse("ads:proposal-update", args=[self.proposal.id]),
            {"status": "accepted"},
        )
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, "accepted")

    def test_proposal_status_update_by_non_receiver(self):
        self.client.login(username=USER1_, password=PASSWORD_)
        response = self.client.post(
            reverse("ads:proposal-update", args=[self.proposal.id]),
            {"status": "accepted"},
        )
        self.assertEqual(response.status_code, 403)


class SearchTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Книги")
        self.condition = Condition.objects.create(name="Б/у")
        self.ad = Ad.objects.create(
            title="Книга по Python",
            description="Продам книгу",
            category=self.category,
            condition=self.condition,
        )

    def test_search_by_keyword(self):
        response = self.client.get(reverse("ads:ad-list") + "?search=Python")
        self.assertContains(response, "Книга по Python")

    def test_filter_by_category(self):
        response = self.client.get(reverse("ads:ad-list") + f"?category={self.category.id}")
        self.assertEqual(len(response.context["ads"]), 1)
