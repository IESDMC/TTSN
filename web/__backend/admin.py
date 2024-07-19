from django.contrib import admin

# Register your models here.
# from .graphql.models import PGA, Building, Event, Station
# from .models import CustomUser

admin.site.site_header = 'TTSN'
admin.site.index_title = 'TTSN'


# @admin.register(CustomUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'is_approved', 'date_joined']
#     fields = ['username', 'email',  'is_approved', 'date_joined']


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in Event._meta.fields]


# @admin.register(Building)
# class BuildingAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in Building._meta.fields]


# @admin.register(Station)
# class StationAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in Station._meta.fields]
#     search_fields = ['code', ]
#     list_per_page = 25


# @admin.register(PGA)
# class EventStationPGAAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in PGA._meta.fields]
