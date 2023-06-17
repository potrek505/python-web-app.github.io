from django.urls import include, path
from django.contrib.auth import views as auth_views
from panel.views import login_view, RegisterView, logout_view




urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('panel/', include('panel.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout')
]
