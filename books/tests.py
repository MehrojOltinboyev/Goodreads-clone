from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response=response, text="No books found")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="desc1", isbn='1')
        book2 = Book.objects.create(title="Book2", description="desc2", isbn='22')
        book3 = Book.objects.create(title="Book3", description="desc3", isbn='333')

        response = self.client.get(reverse("books:list") + "?page_size=2")


        for book in [book1, book2]:
            self.assertContains(response, book.title)

        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list")+"?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):  # ✨ nomini to‘g‘riladik
        book = Book.objects.create(title="Book4", description="desc4", isbn='4')

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))  # ✅ to‘g‘rilandi

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Book1", description="desc1", isbn='1')
        book2 = Book.objects.create(title="Book2", description="desc2", isbn='22')
        book3 = Book.objects.create(title="Book3", description="desc3", isbn='333')


        response = self.client.get(reverse("books:list")+"?q=Book1")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)


class BookReviewTest(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov", email="jrahmonov2@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="jakhongir", password="somepass")

        self.client.post(reverse("books:reviews", kwargs={"id":book.id}), data={
            "stars_given":3,
            "comment":"Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)