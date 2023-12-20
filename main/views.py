from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm, UserForm, ProfileForm, VoteForm
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
import datetime

class ProductAvailabilityView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all()

        available_products = queryset.filter(is_available=True)
        non_available_products = queryset.filter(is_available=False)

        response_data = {
            'metadata': {
                'total_products': queryset.count(),
                'timestamp': datetime.datetime.now().isoformat(),
                'api_version': '1.0'
            },
            'products': {
                'available': self.get_serializer(available_products, many=True).data,
                'non_available': self.get_serializer(non_available_products, many=True).data
            }
        }

        return Response(response_data)

class ProductDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        product = self.get_object()
        if product.stock > 0:
            product.stock -= 1
            product.save()
            return Response({'status': 'stock decreased'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'out of stock'}, status=status.HTTP_400_BAD_REQUEST)

def homepage(request):
	if request.method == "POST":
		product_id = request.POST.get('product_pk')
		product = Product.objects.get(id = product_id)
		request.user.profile.products.add(product)
		messages.success(request,(f'{product} added to wishlist.'))
		return redirect ('main:homepage')
	product = Product.objects.all()[:4]
	return render(request=request, template_name="main/home.html", context={'product':product})


def products(request):
	if request.method == "POST":
		if "score_submit" in request.POST:
			vote_form = VoteForm(request.POST)
			if vote_form.is_valid():
				form = vote_form.save(commit=False)
				form.profile = request.user.profile
				product_id = request.POST.get("product")
				form.product = Product.objects.get(id=product_id)
				form.save()
				form.calculate_averages()
				messages.success(request,(f'{form.product} product score submitted.'))
				return redirect ("main:products")
			messages.error(request,('Form is invalid.'))
			return redirect ("main:products")
		product_id = request.POST.get("product_pk")
		product = Product.objects.get(id = product_id)
		request.user.profile.products.add(product)
		messages.success(request,(f'{product} added to wishlist.'))
		return redirect ('main:products')
	product = Product.objects.all()
	paginator = Paginator(product, 18)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	vote_form = VoteForm()
	return render(request = request, template_name="main/products.html", context = {"product":product, "page_obj":page_obj, "vote_form":vote_form})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="main/register.html", context={"form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("main:homepage")


def userpage(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid():
			user_form.save()
			messages.success(request,('Your profile was successfully updated!'))
		elif profile_form.is_valid():
			profile_form.save()
			messages.success(request,('Your wishlist was successfully updated!'))
		else:
			messages.error(request,('Unable to complete request'))
		return redirect ("main:userpage")
	user_form = UserForm(instance=request.user)
	profile_form = ProfileForm(instance=request.user.profile)
	return render(request = request, template_name ="main/user.html", context = {"user":request.user,
		"user_form": user_form, "profile_form": profile_form })


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            category = form.cleaned_data['category']
            if category:
                products = Product.objects.filter(Q(product_name__icontains=search_term) | Q(product_type__icontains=search_term), product_type=category)
            else:
                products = Product.objects.filter(Q(product_name__icontains=search_term) | Q(product_type__icontains=search_term))
            context = {'products': products}
            return render(request, 'main/search_results.html', context)
    else:
        form = SearchForm()
    return render(request, 'main/search.html', {'form': form})