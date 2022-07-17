import email
from operator import concat
from django.shortcuts import redirect, render, HttpResponse
from blog.models import Post
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    # return HttpResponse('This is homepage')
    allPost = Post.objects.all().filter(active=True).order_by('-created_at')
    context = {'allPost': allPost}
    return render(request, 'website/index.html', context)


def about(request):
    # return HttpResponse('This is about page')
    return render(request, 'website/about.html')


def contact(request):
    # return HttpResponse('This is contact page')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if name and email and phone and message:
            contact = Contact(name=name, email=email,
                              phone=phone, content=message)
            contact.save()
            messages.success(request, 'Message sent successfully!')
        else:
            messages.error(request, 'Please fill up the incomplete fields')

    return render(request, 'website/contact.html')


def frontLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in')
                return redirect("home")
            else:
                messages.warning(
                    request, 'Invalid credentials, please try again with valid credentials.')
        else:
            messages.error(request, 'Username and password field are required')

    return render(request, 'website/login.html')


def frontSignup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('home')

        if not username.isalnum():
            messages.error(
                request, 'User name should only contain letters and numbers')
            return redirect('home')

        if first_name and last_name and username and email and password and confirm_password:
            if password == confirm_password:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.success(request, 'User created successfully!')
                return redirect('home')
            else:
                messages.error(request, "Password didn't matched")
        else:
            messages.error(request, 'Please fill up the required fields')

    return render(request, 'website/signup.html')


def frontLogout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')


def frontSearch(request):
    keyword = request.GET['keyword']
    if not keyword:
        messages.warning(
            request, 'No keyword found, please enter any keyword.')
        return redirect('home')
    if len(keyword) > 70:
        allPosts = Post.objects.none()
        # messages.warning(
        #     request, 'Please enter more keyword for actual result')
        # return redirect('home')
    else:
        allPostTitle = Post.objects.filter(title__icontains=keyword, active=True)
        allPostContent = Post.objects.filter(content__icontains=keyword, active=True)
        allPostAuthor = Post.objects.filter(author__icontains=keyword, active=True)
        # allPosts = allPostTitle.union(allPostContent, allPostAuthor)
        allPosts = (allPostTitle | allPostContent | allPostAuthor).distinct()

    if allPosts.count() == 0:
        messages.warning(
            request, 'No result found! Please refine your keyword')
    params = {'allPosts': allPosts, 'keyword': keyword}
    return render(request, 'website/search.html', params)
