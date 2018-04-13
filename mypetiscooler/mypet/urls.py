from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name ="index"),
    url(r'^addpet/$', views.addpet, name='addpet'),
    url(r'^mypetviews/$', views.viewpet, name='viewpet'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^(?P<petdelete>[0-9]+)/$', views.deletepet, name='deletepet'),
    url(r'^deleteimage/(?P<deleteimg>[0-9]+)/$', views.deletepetimage, name='deletepetimage'),
    url(r'^addphoto/(?P<mypetpk>[0-9]+)$', views.addphoto, name ="addphoto"),
    url(r'^register/$', views.UserFormView.as_view(), name ="register"),
    url(r'^select_petimage/(?P<petid>\d+)/$', views.select_image, name='select_image'),
    url(r'^relative_image/(?P<imageid>[0-9]+)/(?P<species>[a-z.]+)/$', views.select_relativepet, name='select_relativepet'),
    url(r'^total_score/(?P<battle_id>[0-9]+)/(?P<battleinstance>[0-9]+)/$', views.increment_count, name='increment_count'),
    url(r'^currentbattles/$', views.current_battleview, name='current_battleview'),
    url(r'^logout/$', views.logout_view, name='logout_view')
    #url(r'^profile/(?P<username>\w+)/$', 'views.myprofileview', name="detail_profile")

]
