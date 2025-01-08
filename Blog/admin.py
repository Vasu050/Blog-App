from django.contrib import admin
from.models import Todo
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'author_full_name','username','date_created')  
    list_filter = ('author', 'date_created')  
    search_fields = ('title', 'description') 

    def author_full_name(self,user):
        return f"{user.author.first_name} {user.author.last_name}"
    author_full_name.short_description = 'Author'
   
    def username(self, obj):
        return obj.author.username  # Access the 'username' from the 'author' foreign key
    username.short_description = 'Username'
   
admin.site.register(Todo,TodoAdmin)