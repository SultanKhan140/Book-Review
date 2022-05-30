from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Book,Contributor,Review
from .utils import average_book_rating
from .forms import SearchForm,ReviewForm,BookMediaForm
from django.contrib import messages
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    # # value = request.GET.get("name") or "world"
    # # # return HttpResponse("Hello, I am a Response generated")
    # # return HttpResponse("Hello {} !".format(value))
    # # return HttpResponse("Hello World")
    # val = Book.objects.count()
    # message = f"<html><h1>Welcome to Book Review System</h1>"
    # #           "<p>{val} are there in total</p></html>"
    # return HttpResponse(message)
    return render(request,"base.html")


def welcome(request):
    name = "Book Review"
    return render(request,"base.html",{"your_name":name})

def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    # print(f'{form}')
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        lname_contributors = Contributor.objects.filter(last_names__icontains=search)

        for contributor in lname_contributors:
            for book in contributor.book_set.all():
                books.add(book)

    return render(request, "book_search.html", {"form": form, "search_text": search_text, "books": books})



def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")


def book_list(request):
    book_list = Book.objects.all()
    book_with_review = []
    for book in book_list:
        # print(book)
        reviews = book.review_set.all()
        # print("Line 41 : ",reviews)
        if reviews:
            book_rating = average_book_rating([review.rating for review in reviews])
            # print(book_rating)
            number_of_reviews  = len(reviews)
            # print(number_of_reviews)
        else:
            book_rating = None
            number_of_reviews = 0

        book_with_review.append({"book":book,"book_rating":book_rating,"number_of_reviews":number_of_reviews})
        # print(book_with_review)
        # print(f'Book with reviews {book_with_review}')
        content = {
        "book_list":book_with_review
        }

    # return HttpResponse(content['book_list'])
    return render(request,'book_list.html',content)
    # return HttpResponse(book_list)
    # return render(request,"book_list.html")



def book_detail(request,pk):
    '''
    This will give us the detail for a particular book based on the id passed
    '''
    book = get_object_or_404(Book,pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_book_rating([review.rating for review in reviews])
        content = {
            "book":book,
            "book_rating":book_rating,
            "reviews":reviews
        }
    else:
        content = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request,"book_detail.html",content)

@login_required
def review_edit(request,book_pk,review_pk=None):
    book = get_object_or_404(Book,pk=book_pk)
    # print(type(review_pk))
    if review_pk is not None:
        review = get_object_or_404(Review,book_id=book_pk,pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST,instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request,"Review\{}\" was created.".format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request,"Review for\{}\" was updated.".format(book))
            updated_review.save()
            return redirect("book_detail",book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,"instance-form.html",
        {
            "form":form,
            "instance":review,
            "model_type":"Review",
            "related_instance":book,
            "related_model_type":"Book"
        })

@login_required
def book_media(request,pk):
    book = get_object_or_404(Book,pk=pk)
    if request.method == "POST":
        form = BookMediaForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            book = form.save(False)
            cover = form.cleaned_data.get("cover")
            if cover:
                image = Image.open(cover)
                image.thumbnail((300,300))
                image_data = BytesIO()
                image.save(fp=image_data,format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name,image_file)
            book.save()
            messages.success(request, "Book {} was successfully updated".format(book))
            return redirect("book_detail",book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request,"instance-form.html",
                  {
                      "instance":book,
                      "form":form,
                      "model_type": "Book",
                      "is_file_uploaded": True
                  }
                  )


