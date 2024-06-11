from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('register1/', views.register1, name='register1'),
    path('registration/', views.registration, name='registration'),

    path('welcome/', views.welcome, name='welcome'),
    path('delete_stud/<int:id>/', views.delete_stud, name='delete_stud'),
    path('edit_stud/<int:id>/', views.edit_stud, name='edit_stud'),


    path('login1/', views.login1, name='login1'),
    path('login_check/', views.login_check, name='login_check'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),



    # Bank Account
    path('create_account/', views.create_account, name='create_account'),
    path('account_details/<int:account_id>/', views.account_details, name='account_details'),

    # Account Operations
    path('deposit/<int:account_id>/', views.deposit_money, name='deposit_money'),
    path('withdraw/<int:account_id>/', views.withdraw_money, name='withdraw_money'),
    path('transfer/<int:account_id>/', views.transfer_money, name='transfer_money'),

    # Forget Password

    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),



    # User [Employee authentication]

    path('signup/', views.signup, name='signup'),
    path('user_register/', views.user_register, name='user_register'),
    path('signin/', views.signin, name='signin'),

    # Admin Login

    path('admin_login/',views.admin_login, name='admin_login'),
    path('login_panel', views.login_panel, name='login_panel'),



]
