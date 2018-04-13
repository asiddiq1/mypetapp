from django.contrib import admin
from mypet.models import Mypets, MypetsImage, PetBattleImages
# Register your models here.

class MypetsImageInline(admin.TabularInline):
    model = MypetsImage

class MypetsAdmin(admin.ModelAdmin):
    inlines = [
        MypetsImageInline,
    ]

admin.site.register(Mypets, MypetsAdmin)
admin.site.register(PetBattleImages)

#admin.site.register(Mypets)