"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import logout_user, LoginPageView, signup_page
import blog.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPageView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('posts/', blog.views.posts, name='posts'),
    path('signup/', signup_page, name='signup'),
    path('ticket/upload/', blog.views.publier_ticket, name='ticket_upload'),
    path('review/upload/', blog.views.publier_critique, name='review_upload'),
    path('review/ticket/<int:ticket_id>/', blog.views.publier_critique, name='reply_to_ticket'),
    path('subscribe/', blog.views.subscribe, name='subscribe'),
    path('follow_user/<int:user_id>', blog.views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', blog.views.unfollow_user, name='unfollow_user'),
    path('ticket/edit/<int:ticket_id>/', blog.views.edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', blog.views.delete_ticket, name='delete_ticket'),
    path('review/edit/<int:review_id>/', blog.views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', blog.views.delete_review, name='delete_review'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
