from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Artist, Investor

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'full_name', 'phone_number', 'country', 'age', 'is_staff')
    search_fields = ('username', 'email', 'full_name', 'phone_number')

    list_filter = ('is_staff', 'is_active', 'is_superuser', 'country')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'country', 'date_of_birth', 'profile_picture')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'phone_number', 'country', 'date_of_birth', 'profile_picture'),
        }),
    )

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    list_display = ('user_username', 'user_full_name', 'art_section', 'artistic_bio', 'artistic_achievements', 'what_i_need')

    search_fields = ('user__username', 'user__full_name', 'art_section')
 
    list_filter = ('art_section',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def user_full_name(self, obj):
        return obj.user.full_name
    user_full_name.short_description = 'Full Name'


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):

    list_display = ('user_username', 'user_full_name', 'support_type', 'own_art_company', 'company_name', 'company_art_field')

    search_fields = ('user__username', 'user__full_name', 'company_name', 'company_art_field')

    list_filter = ('support_type', 'own_art_company','art_section')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def user_full_name(self, obj):
        return obj.user.full_name
    user_full_name.short_description = 'Full Name'