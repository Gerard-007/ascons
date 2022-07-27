from django.conf import settings
from django.conf.urls.static import  static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import HomeView, AboutView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include(('accounts.api.urls', 'accounts'), namespace='accounts')),
    path('ascons_edu_admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', include(('contacts.urls', 'contacts'), namespace='contacts')),
    path('blogs/', include(('blogs.urls', 'blogs'), namespace='blogs')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('api/blogs/', include(('blogs.api.urls', 'blogs'), namespace='blogs_api')),
    path('api/courses/', include(('courses.api.urls', 'courses'), namespace='courses_api')),
    path('api/events/', include(('events.api.urls', 'events'), namespace='events_api')),
    path('api/contacts/', include(('contacts.api.urls', 'contacts'), namespace='contacts_api')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404.html'))]
