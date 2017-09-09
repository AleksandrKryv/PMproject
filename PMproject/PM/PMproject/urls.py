from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'profiles', views.PMuserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'allprofiles/$', views.AllProfiles.as_view(), name='allprofiles'),
    url(r'profile/(?P<pk>\d+)/$', views.Profile.as_view(), name='profile'),
    url(r'^main/$', views.Main.as_view(), name='main'),
    url(r'main/registration/$', views.registration, name='registration'),
    url(r'profile/model/$', views.modelregistration, name='modelreg'),
    url(r'profile/photograph/$', views.photographregistration, name='photographreg'),
    url(r'login/$', views.userlogin, name='login'),
    url(r'logout/$', views.logoutuser, name='logout'),
    url(r'profile/albums/$', views.Albums.as_view(), name='album'),
    url(r'profile/albums/(?P<pk>\d+)/add$', views.Albums.as_view(), name='add_photo_album'),
    url(r'profile/albums/(?P<pk>\d+)/photo/$', views.Albumview.as_view(), name='photolist'),
    url(r'profile/albums/(?P<pk>\d+)/edit/$', views.changealbum, name='editalbum'),
    url(r'profile/albums/(?P<pk>\d+)/delete/$', views.deleteal, name='deletealbum'),
    url(r'profile/albums/addalbum/$', views.addalbum, name='addalbum'),
    url(r'profile/albums/portfolio/(?P<pk>\d+)/$', views.UserPortfolio.as_view(), name='portfolio'),
    url(r'profile/albums/portfolioedit/$', views.edit_portfolio, name='portfolioedit'),
    url(r'profile/albums/portfolio/change$', views.changeportfoliodescription, name='portfoliochange'),
    url(r'profile/albums/portfolio/addalbums/$', views.PortfolioAlbumAdd.as_view(), name='portfolioalb'),
    url(r'profile/albums/portfolio/addphoto/$', views.PortfolioPhotoAdd.as_view(), name='portfoliophoto'),
    url(r'profile/albums/portfolio/delphoto/$', views.portfolio_photo_delete, name='portfoliophotodelete'),
    url(r'profile/extend/$', views.extendprofile, name='extend'),
    url(r'profile/like/(?P<pk>\d+)$', views.like, name='like'),
    url(r'profile/dislike/(?P<pk>\d+)$', views.dislike, name='dislike'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
      + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

