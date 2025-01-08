# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import Todo#,BlogImage
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

def blog(request):

    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
      
    if request.method == 'POST': 
        title = request.POST.get('title')   
        description = request.POST.get('description')
        img = request.FILES.get('img')
        author=request.user
        new_blog = Todo(
            title=title,
            description=description,
            author=author,
            img=img
        )

        try:
            new_blog.save()  
            return redirect('/blog/blogs/')  
        except Exception as e:
           
            return f'error: {str(e)}'

    blogs = Todo.objects.filter(author=request.user).order_by('-date_created')  
    return render(request, 'index.html', {'blogs': blogs})
       
def delete_blog(request,id):
        if not request.user.is_authenticated:  
            messages.error(request, 'Authentication Required')
            return redirect('/')
        blog_to_delete = get_object_or_404(Todo,id=id,author=request.user)  
        try:
            blog_to_delete.delete() 
              
        except Exception as e:
            return f'There was a problem deleting that blog: {str(e)}'
        
        return redirect('/blog/blogs/') 
     

def update_blog(request,id):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
    
    blog = get_object_or_404(Todo,id=id,author=request.user)  
    if request.method == 'POST':  
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        if request.FILES.get('img'):
            blog.img = request.FILES.get('img')
       
        try:
            blog.save()  
            return redirect('/blog/blogs/')  
        except Exception as e:
            return f'There was an issue updating your blog: {str(e)}' 
    
    else:
        return render(request, 'update.html', {'blog': blog})

    
# @loginrequired
def add_blog(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
    
    if request.method == 'POST':

        '''title = request.POST['title']
        description = request.POST['description']
        author = request.user
       
        new_blog = Todo(title=title, description=description, author=author)
        new_blog.save() '''

        return redirect('/blog/blogs/')  
    return render(request, 'add.html')


def blog_detail(request,id):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
    
    blog = get_object_or_404(Todo, id=id)
    return render(request, 'blog_detail.html', {'blog': blog})


def search(request):
    if request.method=='POST':
        query = request.POST.get('query','')
        source = request.POST.get('source', '')
        
    if source=='/blog/blogs/':
        blogs = Todo.objects.filter(
        Q(title__icontains=query) | Q(author__first_name__icontains=query) 
        | Q(author__last_name__icontains=query) | Q(description__icontains=query),author=request.user)
        return render(request,'myblog.html',{'blogs': blogs})
    else:
        blogs = Todo.objects.filter(
        Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query) | Q(description__icontains=query))
        return render(request,'ht.html',{'blogs': blogs})


def myblogs(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')

    blogs = Todo.objects.order_by('-date_created') 
    paginator = Paginator(blogs, 4)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 

    return render(request, 'ht.html', {'page_obj': page_obj,'blogs': blogs})
  #  return render(request, 'ht.html', {'blogs': blogs})


'''@csrf_exempt
def upload_image(request, blog_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required.'})

    if request.method == 'POST':
        blog = get_object_or_404(Todo, id=blog_id, author=request.user)
        image = request.FILES.get('img')

        if image:
            BlogImage.objects.create(blog=blog, image=image)
            return JsonResponse({'success': True, 'message': 'Image uploaded successfully!'})
        return JsonResponse({'success': False, 'message': 'No image provided.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def upload_images_page(request, blog_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Authentication Required')
        return redirect('/')

    blog = get_object_or_404(Todo, id=blog_id, author=request.user)
    return render(request, 'upload_images.html', {'blog': blog})
'''