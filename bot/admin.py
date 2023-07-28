from django.contrib import admin
from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(CakeConstructor)
class CakeConstructorAdmin(admin.ModelAdmin):
    pass


@admin.register(LinkStatistics)
class LinkStatisticsAdmin(admin.ModelAdmin):
    readonly_fields = ('transitions',
                       'bitlink')
    list_display = ('description',
                    'bitlink',
                    'transitions')


