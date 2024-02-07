from django.urls import path, include
from . import views
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    #path("api-token-auth", obtain_auth_token),
    #path("menu-items", views.menu_items),
    path("groups/", views.GroupView.as_view()),
    path("category/", views.CategoryView.as_view()),
    
    path("menu-items", views.MenuItemView.as_view()),
    path("menu-items/<int:pk>", views.SingleItemView.as_view()),
    
    path("groups/manager/users", views.ManagerViewSet.as_view({
        "get" : "list",
        "post": "create", 
        "delete": "destroy"    
    })),
    path("groups/delivery-crew/users", views.DeliveryCrewViewSet.as_view(
        {
            "get": "list",
            "post": "create",
            "delete": "destroy"
    })),
    #path("cart/menu-items", views.cart),
    path("cart/menu-items", views.CartView.as_view()),
    # path("cart/menu-items", views.CartViewSet.as_view({
    #     'post': 'create',
    #     'get': 'list',
    #     'delete': 'destroy'
    # })),
    
    path("orders", views.OrdersView.as_view(
        # {
        #     'post': 'create',
        #     'get': 'list',
        #     'delete': 'destroy'
        # }
        )),
    # path("orders/<int:id>", views.OrderItemViewSet.as_view({
    #     'get': 'list',
    # })),
    path("orders/<int:pk>", views.SingleOrderView.as_view()),
    #path("auth-error", views.auth_error)
]