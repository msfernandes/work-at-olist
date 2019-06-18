from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.urls import router

schema_view = get_schema_view(
    openapi.Info(
        title="Olist Call API",
        default_version='v1',
        description="This API was made as a test for a job application"
                    " at Olist",
        contact=openapi.Contact(email="matheus.souza.fernandes"),
    ),
    public=True,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
]
