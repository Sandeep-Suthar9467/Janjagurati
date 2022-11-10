from django.urls import path
from .views import (
    home,
    SchemeListView,
    SchemeDetailView,
    SchemeAdd,
    tagged
)
# from . import views
urlpatterns = [
    path('', home, name='home'),
    path('schemes/', SchemeListView.as_view(), name='schemes'),
    path("schemes/<slug:slug>/",SchemeDetailView.as_view(), name='schemedetail'),
    path('add-scheme/',SchemeAdd.as_view(),name = 'addscheme'),
    path('tagged/<slug:slug>',tagged,name='tagged')
]