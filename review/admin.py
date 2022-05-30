from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Publisher,Contributor,Book,BookContributor,Review
from django.contrib.auth.models import Group,User

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title','isbn13')
    list_filter = ('publisher','publication_date')
    search_fields = ('title','isbn','publisher__name')

class BookAdminSite(AdminSite):
    title_header = 'Book Review Admin'
    site_header = 'Book Review Administrator Panel'
    index_title = 'Book Review Site Admin'
    site_title = 'Book Admin Panel'


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('first_names','last_names')
    list_filter = ('last_names',)
    search_fields = ('first_names',)




admin_site = BookAdminSite(name='Bookr')
# Register your models here.
admin_site.register(Publisher)
admin_site.register(Contributor,ContributorAdmin)
admin_site.register(Book,BookAdmin)
admin_site.register(BookContributor)
admin_site.register(Review)
admin_site.register(Group)
admin_site.register(User)

