from django.urls import path
from . import views
from django.urls import path
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from verilog_app.views import compile_verilog
schema_view = get_schema_view(
    openapi.Info(
        title="Verilog Compiler API",
        default_version='v1',
        description="API for compiling Verilog code",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('compile/', views.compile_verilog, name='compile_verilog'),
]
