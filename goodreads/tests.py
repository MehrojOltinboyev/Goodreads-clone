from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book1 = Book.objects.create(title="Book1", description="desc1", isbn='1')
        user = CustomUser.objects.create(
            username="jakhongir",
            first_name="Jakhongir",
            last_name="Rakhmonov",
            email="jrahmonv2@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        review1 = BookReview.objects.create(book=book1, user=user, stars_given=3, comment="Super!")
        review2 = BookReview.objects.create(book=book1, user=user, stars_given=5, comment="Amazing!")
        review3 = BookReview.objects.create(book=book1, user=user, stars_given=4, comment="Perfect!")

        # 2 ta element per page, 2-sahifani chaqiramiz
        response = self.client.get(reverse("home_page") + "?page=2&page_size=2")

        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)
        self.assertNotContains(response, review2.comment)
