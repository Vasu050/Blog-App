from django.contrib import admin
from django.urls import path
from Blog import views
urlpatterns = [
    path('blogs/', views.blog, name='blog'),
    path('delete/<int:id>/', views.delete_blog, name='delete_blog'),
    path('update/<int:id>/', views.update_blog, name='update_blog'),
    path('add/',views.add_blog,name='add_blog'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('search/',views.search,name='query'),
    path('myblogs/',views.myblogs,name='myblogs'),
    #path('upload-image/<int:blog_id>/', views.upload_image, name='upload_image'),
    #path('upload-images/<int:blog_id>/', views.upload_images_page, name='upload_images_page'),
    
]
