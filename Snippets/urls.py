from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="snippets-add"),
    path('snippets/delete/<int:id>/', views.snippets_delete, name="snippets-delete"),
    path('snippets/edit/<int:id>/', views.snippets_edit, name="snippets-edit"),
    path('snippets/list', views.snippets, name="snippets-list"),
    path('snippet/<int:id>', views.snippet_page, name="snippet"),
    path('snippets/my', views.snippets_my, name="snippets-my"),

    path('auth/login/', views.login, name="login"),
    path('auth/logout/', views.logout, name="logout"),
    path('auth/register/', views.register, name="register"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)