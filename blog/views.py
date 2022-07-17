from unicodedata import category, name
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import Post, Category
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.


def blogs(request):
    # return HttpResponse('This is blogs page')
    allBlogs = Post.objects.all().filter(active=True).order_by('-created_at')
    context = {'allPosts': allBlogs}
    return render(request, 'blog/blogs.html', context)


def blogDetail(request, slug):
    # return HttpResponse('This is blog detail page')
    post = Post.objects.filter(slug=slug, active=True).first()
    if post:
        post.views = post.views + 1
        post.save()
        context = {'post': post}
        return render(request, 'blog/blogDetail.html', context)
    else:
        return redirect('home')


def uploadBlog(request):
    # return render(request, 'blog/uploadBlog.html')
    allCategories = Category.objects.filter(active=True).all()
    print(allCategories)
    if request.user.is_authenticated:
        print(request.FILES)
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            isCategory = request.POST['category']
            # image = request.POST['featured_image']
            # upolad = request.FILES['featured_image']
            # upolad = request.POST.get('featured_image', False)
            image = ''
            upolad = request.FILES['featured_image'] if 'featured_image' in request.FILES else None
            if upolad:
                fs = FileSystemStorage(location='static/media/blogs/')
                file = fs.save(upolad.name, upolad)
                image = 'blogs' + fs.url(file)

            if title and content and isCategory:
                try:
                    category = get_object_or_404(Category, id=isCategory)
                    # category = Category.objects.filter(
                    #     category_id=isCategory, active=True).first()
                    post = Post(category=category,
                                title=title, content=content, image=image, author=request.user)
                    post.save()
                    messages.success(request, 'Blog submitted successfully!')
                    return redirect('home')
                except:
                    messages.warning(
                        request, 'Something went wrong, Please try again!')

                # category = Category.objects.filter(name=isCategory)
                # category = Category.objects.filter(
                #     name=isCategory, active=True).first()
                # if not category:
                #     categoryArr = Category(name=isCategory, active=False)

            else:
                messages.error(request, "All field are required")

        context = {'allCategories': allCategories}
        return render(request, 'blog/uploadBlog.html', context)
    else:
        return render(request, 'website/login.html')
