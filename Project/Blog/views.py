# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import Todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
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

    

def add_blog(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
    
    if request.method == 'POST':
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
        request.session['query'] = query
        request.session['source'] = source
    else:
        query = request.session.get('query', '')
        source = request.session.get('source', '')

    if source=='/blog/blogs/':
        blogs = Todo.objects.filter(
        Q(title__icontains=query) | Q(author__first_name__icontains=query) 
        | Q(author__last_name__icontains=query) | Q(description__icontains=query),author=request.user)
        return render(request,'index.html',{'blogs': blogs})
    else:
        blogs = Todo.objects.filter(
        Q(title__icontains=query) | Q(author__first_name__icontains=query) 
        | Q(author__last_name__icontains=query) | Q(description__icontains=query)).order_by('-date_created')  
        page_obj = pagination(request,blogs)
        
        return render(request, 'ht.html', {'page_obj': page_obj, 'query': query, 'source': source})


def myblogs(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')

    blogs = Todo.objects.order_by('-date_created') 
    page_obj = pagination(request,blogs)
    return render(request, 'ht.html', {'page_obj': page_obj,'blogs': blogs})

def pagination(request,blogs):
    
    paginator = Paginator(blogs, 4)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    return page_obj
