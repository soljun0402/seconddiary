from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def my_view(request):
  ...
  
def cover(request):
  blogs = Blog.objects.all()
  count = Blog.objects.all().count()
  return render(request, 'cover.html', {'blogs':blogs, 'count':count})

def home(request):
  blogs = Blog.objects.order_by('-pub_date')
  paginator = Paginator(blogs, 5)
  page = request.GET.get('page')
  blogs = paginator.get_page(page)
  return render(request, 'home.html', {'blogs':blogs})

def detail(request, id):
  blog = get_object_or_404(Blog, pk = id)
  return render(request, 'detail.html', {'blog':blog})

def new(request):
  form =BlogForm()
  return render(request, 'new.html',{'form':form})

def create(request):
  # new_blog = Blog()
  # new_blog.title = request.POST['title']
  # new_blog.writer = request.POST['writer']
  # new_blog.body = request.POST['body']
  # new_blog.pub_date = timezone.now()
  # new_blog.image = request.FILES['image']
  # new_blog.save()
  form = BlogForm(request.POST, request.FILES)
  if form.is_valid():
    new_blog = form.save(commit=False)
    new_blog.pub_date = timezone.now()
    new_blog.save()
    return redirect('detail', new_blog.id)
  return redirect('home')

def edit(request, id):
  edit_blog = Blog.objects.get(id= id)
  return render(request, 'edit.html', {'blog':edit_blog})

def update(request, id):
  update_blog = Blog.objects.get(id= id)
  update_blog.title = request.POST['title']
  # update_blog.writer = request.POST['writer']
  update_blog.body = request.POST['body']
  update_blog.pub_date = timezone.now()
  update_blog.save()
  return redirect('detail', update_blog.id)

def delete(request, id):
  delete_blog = Blog.objects.get(id= id)
  delete_blog.delete()
  return redirect('home')

def menu(request):
  blogs = Blog.objects.all()
  return render(request, 'menu.html')