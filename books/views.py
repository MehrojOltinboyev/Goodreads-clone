from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from books.forms import BookReviewForm
from books.models import Book, BookReview


# Create your views here.

# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q','')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get("page_size", 2)
        paginator = Paginator(object_list=books, per_page=page_size)


        page_num = request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)

        return render(
            request=request,
            template_name='books/list.html',
            context={"page_obj":page_obj, "search_query": search_query}
        )



class BookDetailView(View):
    def get(self,request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        return render(request=request, template_name='books/detail.html', context={'book':book, "review_form":review_form})


class AddReviewView(LoginRequiredMixin,View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment']
            )
            return redirect(reverse("books:detail", kwargs={"id":book.id}))

        return render(request, "books/detail.html", {"book":book, "review_form":review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):

        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {"book":book, "review":review, "review_form":review_form}

        return render(request=request, template_name='books/edit_review.html', context=context)

    def post(self, request, book_id, review_id):

        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request=request, template_name='books/edit_review.html', context={"book":book, "review":review, "review_form":review_form})



class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        return render(request=request, template_name="books/confirm_delete_review.html", context={"book":book, "review":review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)


        review.delete()
        messages.success(request=request, message="You have successfully deleted this comment")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))