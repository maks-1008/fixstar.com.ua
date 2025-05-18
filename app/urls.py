from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from debug_toolbar.toolbar import debug_toolbar_urls
from app.settings import DEBUG
from app.admin_customization import customize_admin

# Настраиваем админку
customize_admin()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("", include(("goods.urls", "goods"), namespace="goods")),
    path("user/", include("users.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("orders/", include("orders.urls")),
    path("cart/", include("carts.urls", namespace="cart")),
    path("i18n/setlang/", set_language, name="set_language"),
    # Добавляем явные обработчики для страниц ошибок, чтобы их можно было просматривать в режиме DEBUG=True
    path("404/", TemplateView.as_view(template_name="404.html"), name="page_404"),
    path("500/", TemplateView.as_view(template_name="500.html"), name="page_500"),
    path("403/", TemplateView.as_view(template_name="403.html"), name="page_403"),
]

# Добавляем обработку медиа-файлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Добавляем обработку статических файлов
urlpatterns += staticfiles_urlpatterns()
