from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from store.forms import *
from django.http import Http404
import datetime
# Create your views here.

def index(request):
	return render(request, 'store/index.html')

def bookDetailView(request, bid):
	template_name = 'store/book_detail.html'
	book=Book.objects.filter(id=bid).first()
	num_available=BookCopy.objects.filter(book=book).filter(status=True).count()
	context = {
		'book': book, # set this to an instance of the required book
		'num_available': num_available, # set this to the number of copies of the book available, or 0 if the book isn't available
	}
	
	return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
	template_name = 'store/book_list.html'
	get_data = request.GET
	
	books = Book.objects.all()
	if 'title' in get_data.keys():
		books = books.filter(title__icontains = get_data['title'])
	if 'author' in get_data.keys():
		books = books.filter(author__icontains = get_data['author'])
	if 'genre' in get_data.keys():
		books = books.filter(genre__icontains = get_data['genre'])

	context = {
		'books': books,
	}
	return render(request, template_name, context=context)



@login_required
def viewLoanedBooks(request):
	template_name = 'store/loaned_books.html'
	books=BookCopy.objects.filter(borrower=request.user)
	'''
	The above key 'books' in the context dictionary should contain a list of instances of the 
	BookCopy model. Only those book copies should be included which have been loaned by the user.
	'''
	context = {
		'books': books,
	}

	return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
	'''
	Check if an instance of the asked book is available.
	If yes, then set the message to 'success', otherwise 'failure'
	'''
	if request.method == 'POST':
		message=''
		book_id = request.POST.get('bid') # get the book id from post data
		book=Book.objects.filter(id=book_id).first()
		loan=BookCopy.objects.filter(book=book).filter(status=True)
		if loan.count()!=0:
			loan=loan.first()
			loan.status=False
			loan.borrower=request.user
			loan.borrow_date=datetime.date.today() 
			loan.save()
			message='success'
		else:
			message='failure'
	
		response_data = {
			'message': message,
		}
		return JsonResponse(response_data)
	else :
		 raise Http404("Error :(")

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
	if request.method=='POST':
		book_id=request.POST.get('bid')

		book=BookCopy.objects.filter(id=book_id).first()
		if book.status == False:
			book.borrow_date=None
			book.borrower=None
			book.status=True
			book.save()
			message='success'
		else :
			message='failure'

		response_data={
			'message':message,
		}
		return JsonResponse(response_data)
	else :
		raise Http404("Error :(")


@csrf_exempt
@login_required
def rating(request,bid):

	template_name='store/rating.html'
	if request.method=='POST':

		form=RatingForms(request.POST)
		total_rating = 0
		if form.is_valid():

			new_rating = float(request.POST.get('rating'))	
			book = Book.objects.filter(id=bid).first()

			total_user_ratings = BookRating.objects.filter(book=book)
			total_rating = 0

			for user_ratings in total_user_ratings :
				total_rating += user_ratings.ratings

			user_book = BookRating.objects.filter(book=book,user=request.user)

			if user_book.count() !=0:
				user_book=user_book.first()
				total_rating += (new_rating - user_book.ratings)	
				total_rating /= total_user_ratings.count()

			else :
				new_user=BookRating(book=book ,	user=request.user , ratings=new_rating)
				total_rating += new_rating
				total_rating /= (total_user_ratings.count()+1)
				new_user.save()

			book.rating = total_rating
			book.save()
			context ={
				'book': book, 
			}


		return render(request, template_name, context=context)

	else :
		raise Http404("Error :(")
			
@csrf_exempt

def signup(request):

	form= SignupForms(request.POST)
	# template_name='registration/login.html'
	if request.method=='POST':
		
		if form.is_valid():
			form.save()
			return redirect('/accounts/login')

	else:
		form = SignupForms()
	
	return render(request, 'registration/signup.html', {'form': form})


