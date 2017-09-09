from django.contrib import admin
from .models import PMuser, Comment, Photograph, Model, Photo, Portfolio, Album, Like
from django.contrib import admin
from django.contrib.contenttypes.admin import *
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail


class usertypefilter(admin.SimpleListFilter):
    title = 'user type'

    parameter_name = 'Type'

    def lookups(self, request, model_admin):
        return (
            ('photograph', ('Photographs')),
            ('model', ('Models')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'photograph':
            return queryset.filter(photograph__username__isnull=False)
        if self.value() == 'model':
            return queryset.filter(model__username__isnull=False)


class ModelInLine(admin.StackedInline):
    model = Model
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('about', ('height', 'hair_color', 'eye_color'),
                       ('body_type', 'skin_tone', 'hair_length'), 'level', 'experience', 'conditions', 'likes',
                       ), }),)
    readonly_fields = ('likes',)


class PhotographInLine(admin.StackedInline):
    model = Photograph
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('about', ('experience', 'level'), 'conditions', 'likes')
        }),
    )
    readonly_fields = ('likes',)


class PMuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'country', 'city', 'number', 'likes', 'thumb')
    inlines = [ModelInLine, PhotographInLine]
    list_filter = (usertypefilter,)
    fieldsets = (
        (None, {
            'fields': ('photo', ('username', 'password',),
                       "first_name", "last_name",
                       'gender', 'age',
                       ('date_joined', 'last_login'),
                       'email', ('country', 'city',), 'phone_number',
                       'preferences', 'likes', 'is_staff', "is_active",)
        }),
    )
    readonly_fields = ('date_joined', 'last_login',)
    search_fields = ['username', 'city', 'country', ]

    def thumb(self, user):
        if user.photo:
            return user.photo.thumb()
        else:
            return " "

    thumb.short_description = 'Profile Photo'
    thumb.allow_tags = True


class GenericInlineModelAdmin(GenericTabularInline):
    model = Comment
    extra = 0


class ModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'level', 'conditions', 'likes')
    fieldsets = (
        (None, {
            'fields': ('about', ('height', 'hair_color', 'eye_color'),
                       ('body_type', 'skin_tone', 'hair_length'),
                       'level', 'experience', 'conditions', 'likes',
                       ), }),)
    readonly_fields = ('likes',)
    inlines = [GenericInlineModelAdmin]


class PhotographAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'level', 'conditions', 'likes',)
    fieldsets = (
        (None, {
            'fields': ('about', ('experience', 'level'), 'conditions', 'likes')
        }),
    )
    readonly_fields = ('likes',)
    inlines = [GenericInlineModelAdmin]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'text')


class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
        list_display = ('photo_name', 'thumb', 'photographs', 'models', 'likes')
        inlines = [GenericInlineModelAdmin]



class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'album_name', 'likes')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user')


admin.site.register(PMuser, PMuserAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Like, LikeAdmin)
