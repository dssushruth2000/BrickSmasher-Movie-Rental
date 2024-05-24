from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Movie, User, Checkout
import json
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'rental/home.html')

@csrf_exempt
def account_creation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")

        if not first_name or not last_name or not email:
            return JsonResponse({"error": "All fields are required."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Error: Email already exists."}, status=400)

        User.objects.create(first_name=first_name, last_name=last_name, email=email)
        return JsonResponse({"message": "Account created successfully."})

    
    return render(request, 'rental/account.html')

@csrf_exempt
def manage_movies(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            title = data.get("title", "").strip()
            movie_id = data.get("movie_id")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")

        message = ""
        if action == "new" and title:
            if Movie.objects.filter(title=title).exists():
                return JsonResponse({"error": "Movie title already exists."}, status=400)
            Movie.objects.create(title=title, in_stock=1)
            message = "Movie added successfully."

        elif action == "add" and movie_id:
            movie = get_object_or_404(Movie, id=movie_id)
            movie.in_stock += 1
            movie.save()
            message = "In-stock count increased."

        elif action == "remove" and movie_id:
            movie = get_object_or_404(Movie, id=movie_id)
            if movie.in_stock > 0:
                movie.in_stock -= 1
                movie.save()
                message = "In-stock count decreased."
            else:
                return JsonResponse({"error": "Cannot decrease stock below zero."}, status=400)

        else:
            return JsonResponse({"error": "Invalid action or missing data."}, status=400)

        return JsonResponse({"message": message})

    
    movies = Movie.objects.all().order_by("title")
    return render(request, 'rental/movies.html', {"movies": movies, "message": ""})

def rent_return_movies(request):
    email = request.GET.get("email")
    user = User.objects.filter(email=email).first() if email else None
    
    
    
    member_info = f"{user.first_name} {user.last_name} ({user.email})" if user else ''
    
    
    rentals = []
    if user:
        user_rentals = Checkout.objects.filter(user=user)
        rentals = [
            {"id": rental.id, "title": rental.movie.title, "user_id": rental.user.id, "movie_id": rental.movie.id}
            for rental in user_rentals
        ]
    
    
    all_movies = Movie.objects.filter(in_stock__gt=0).order_by("title")
    movies = [
        {"id": movie.id, "title": movie.title, "in_stock": movie.in_stock}
        for movie in all_movies
    ]
    
    
    if not email:
        return render(request, 'rental/rent.html', {"all_movies": all_movies})
    
    
    return JsonResponse({
        "member_info": member_info,
        "rentals_list": rentals,
        "all_movies_list": movies,
        "user_id": user.id if user else None
    })


@csrf_exempt
def manage_rentals(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")
        action = data.get("action")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")

    if not user_id or not movie_id:
        return JsonResponse({"error": "Missing or invalid user or movie ID."}, status=400)

    try:
        user = get_object_or_404(User, id=user_id)
        movie = get_object_or_404(Movie, id=movie_id)
    except ValueError:
        return JsonResponse({"error": "Invalid user or movie ID."}, status=400)

    if action == "rent":
        
        if Checkout.objects.filter(user=user, movie=movie).exists():
            return JsonResponse({"error": "You have already rented this movie."}, status=400)

        
        if Checkout.objects.filter(user=user).count() >= 3:
            return JsonResponse({"error": "You can't rent more than 3 movies."}, status=400)

        
        if movie.in_stock <= 0:
            return JsonResponse({"error": "This movie is out of stock."}, status=400)

       
        Checkout.objects.create(user=user, movie=movie)
        movie.in_stock -= 1
        movie.save()
        message = f"'{movie.title}' rented successfully."

    elif action == "return":
        rental = Checkout.objects.filter(user=user, movie=movie).first()
        if rental:
            rental.delete()
            movie.in_stock += 1
            movie.save()
            message = f"'{movie.title}' returned successfully."
        else:
            message = "Error: Could not find the rented movie record."

    
    all_movies = Movie.objects.filter(in_stock__gt=0).order_by("title")
    all_movies_list = ''.join([
        f"<li>{movie.title} ({movie.in_stock} available) <button onclick='submitRental(\"rent\", {user.id}, {movie.id})'>Rent</button></li>"
        if movie.in_stock > 0 else f"<li>{movie.title} (Out of Stock)</li>"
        for movie in all_movies
    ])

    return JsonResponse({
        "message": message,
        "all_movies_list": all_movies_list
    })