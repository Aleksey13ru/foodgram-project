from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('about-term/', views.flatpage,
         {'url': '/about-term/'}, name='about-term'),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='about-spec'),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('api/v1/', include('api.urls')),
    path('', include('recipes.urls')),
]

# urlpatterns += [
#     path('about-term/', views.flatpage,
#          {'url': '/about-term/'}, name='about-term'),
#     path('about-author/', views.flatpage,
#          {'url': '/about-author/'}, name='about-author'),
#     path('about-spec/', views.flatpage,
#          {'url': '/about-spec/'}, name='about-spec'),
# ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

handler404 = 'recipes.views.page_not_found' # noqa
handler500 = 'recipes.views.server_error' # noqa
