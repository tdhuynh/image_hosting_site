from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from image_host_app.views import PostListView, UserCreateView, PostCreateView, ProfileListView, \
                                 PostDetailView, PostUpdateView, CommentCreateView, CommentUpdateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', UserCreateView.as_view(), name='user_create_view'),
    url(r'^$', PostListView.as_view(), name='post_list_view'),
    url(r'^create_post/$', PostCreateView.as_view(), name='post_create_view'),
    url(r'^accounts/profile/$', ProfileListView.as_view(), name='profile_list_view'),
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail_view'),
    url(r'^post/(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name='post_update_view'),
    url(r'^post/(?P<pk>\d+)/comment/$', CommentCreateView.as_view(), name='comment_create_view'),
    url(r'^comment/(?P<pk>\d+)/update$', CommentUpdateView.as_view(), name='comment_update_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
