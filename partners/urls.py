from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', views.index, name='index'), 
    path('add-partner/', views.add_partner, name='add_partner'),
    path('partner-list/', views.partner_list, name='partner_list'),
    path('filter-partners/', views.filter_partners, name='filter_partners'),
    path('add-osloveni/', views.add_osloveni, name='add_osloveni'),
    path('partners-summary/', views.partners_summary, name='partners_summary'), 
    path('osloveni-detail/<int:osloveni_id>/', views.osloveni_detail, name='osloveni_detail'),
    path('logout/', LogoutView.as_view(next_page='/logoutpage/'), name='logout'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
