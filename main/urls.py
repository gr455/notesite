"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views

app_name  = "main"

urlpatterns = [
	path("", views.homepage, name = "homepage"),
    path("preconfirm/", views.preconfirm, name = "preconfirm"),
	path("register/", views.register, name = "register"),
    path('users/validate/<username>/<token>', views.activate_user, name='user-activation'),
	path("logout/", views.logout_user, name = "logout"),
	path("login/", views.login_user, name = "login"),
    path("create/", views.create, name = "create"),
    path("users/", include([
            path("<uname>/", include([
                    path("", views.view_user, name = "user"),
                    path("settings/changename", views.change_name, name = "change-name"),
                    path("settings/changepass", views.change_pass, name = "change-password"),
                    path("settings/", views.user_settings, name = "user-settings")
                ]))

        ])),
    path('<var>/', include([

        path("", views.direct_path, name = "path"),
        path("<var2>/", include([
            path("", views.indirect_path, name = "ipath"),
            path("<var3>/", include([
            	path("", views.show, name = "show"),
            	path("open", views.open_document, name = "open")

            	])),
        ])),

    ])),
]
