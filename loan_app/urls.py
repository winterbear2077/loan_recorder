from django.urls import path, re_path
from . import views
app_name = 'loan_app'
urlpatterns = [
    path("", views.index, name='index'),
    path("<uuid:user_id>/loans", views.detail, name='detail'),
    re_path(r'^.*$', views.handle_404_default, name='not-found')
]
