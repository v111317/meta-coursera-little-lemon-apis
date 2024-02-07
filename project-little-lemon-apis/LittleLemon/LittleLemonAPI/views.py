
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

from .permissions import IsDeliveryCrew, IsManager
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import OrderItemSerializer, OrderSerializer, CartSerializer, MenuItemSerializer, GroupSerializer, UserSerializer, CategorySerializer
from .paginations import MenuItemPagination
from django.core.paginator import Paginator, EmptyPage

# def is_manager(user):
#     return user.groups.filter(name="Manager").exists()

# def is_delivery_crew(user):
#     return user.groups.filter(name="Delivery Crew").exists()

@api_view(['GET'])
def auth_error(request):
    return Response({"message": "authorization failed"}, status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET', 'POST'])
# @user_passes_test(is_delivery_crew, login_url="/api/auth-error")
# def menu_items(request):
#     if request.method == "GET":
#         items = MenuItem.objects.select_related("category").all()
#         serialized_items = MenuItemSerializer(items, many=True)
#         return Response(serialized_items.data, status.HTTP_200_OK)
    
#     if request.method == "POST":
#         serialized_items = MenuItemSerializer(data=request.data)
#         serialized_items.is_valid(raise_exception=True)
#         serialized_items.save()
#         return Response(serialized_items.data, status.HTTP_201_CREATED)   

class GroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser | IsManager]
    serializer_class = GroupSerializer

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser | IsManager]
        return super(CategoryView, self).get_permissions()


class MenuItemView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    ordering_fields = ["price"]
    search_fields = ["title", "category__title"]
    pagination_class = MenuItemPagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
        return super(MenuItemView, self).get_permissions()
    
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def single_item(request, id):
#     item = get_object_or_404(MenuItem, pk=id)
    
#     if request.method == "GET":    
#         serialized_item = MenuItemSerializer(item)
#         return Response(serialized_item.data)
    
#     if request.method == "PUT" or request.method == "PATCH":
#         #partial =True allows for partial updation
#         serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
#         #print(serialized_item)
#         if serialized_item.is_valid():
#             serialized_item.save()
#             return Response(serialized_item.data)
#         return Response(serialized_item.errors, status.HTTP_400_BAD_REQUEST)
    
#     if request.method == "DELETE":
#         item.delete()
#         return Response({"message": "deleted"}, status.HTTP_200_OK)

class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        method = self.request.method
        if method in ["POST", "PUT", "DELETE"]:
            self.permission_classes = [IsAuthenticated, IsManager]
        return super(SingleItemView, self).get_permissions()        

# @api_view(["GET", "POST", "DELETE"])
# def managers(request):
#     req_method = request.method
#     if req_method == "GET":
#         managers = Group.objects.get(name="Manager")
#         users = managers.user_set.all()
#         #print(users)
#         #serialized_items = GroupSerializer(users, many=True)
#         serialized_items = UserSerializer(users, many=True)
#         #serialized_items = json.dumps(users, cls=DjangoJSONEncoder)
#         return Response(serialized_items.data)
        
#     elif req_method == "POST" or req_method == "DELETE":
#         username = request.data['username']
#         if username:
#             user = get_object_or_404(User, username=username)
#             if req_method == "POST":
#                 managers.user_set.add(user)
#             if req_method == "DELETE":
#                 managers.user_set.remove(user)
#             return Response({"message": "ok"}, status.HTTP_200_OK)

class ManagerViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    
    def list(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        manager_gp = Group.objects.get(name="Manager")
        manager_gp.user_set.add(user)
        return Response({"message": "Added to Manager group"}, status.HTTP_201_CREATED)

    def destroy(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        manager_gp = Group.objects.get(name="Manager")
        manager_gp.user_set.remove(user)
        return Response({"message": "Removed from Manager group"}, status.HTTP_201_CREATED)
        
# @api_view(["GET", "POST", "DELETE"])
# def delivery_crew(request):
#     req_method = request.method
#     delivery_crew = Group.objects.get(name="Delivery_Crew")
#     if req_method == "GET":
#         users = delivery_crew.user_set.all()
#         #print(users)
#         #serialized_items = GroupSerializer(users, many=True)
#         serialized_items = UserSerializer(users, many=True)
#         #serialized_items = json.dumps(users, cls=DjangoJSONEncoder)
#         return Response(serialized_items.data)
        
#     elif req_method == "POST" or req_method == "DELETE":
#         username = request.data['username']
#         if username:
#             user = get_object_or_404(User, username=username)
#             if req_method == "POST":
#                 delivery_crew.user_set.add(user)
#             if req_method == "DELETE":
#                 delivery_crew.user_set.remove(user)
#             return Response({"message": "ok"}, status.HTTP_200_OK)

class DeliveryCrewViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAdminUser | IsManager]
    
    def list(self, request):
        crew = User.objects.filter(groups__name="Delivery Crew")
        serializer = UserSerializer(crew, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        crew = Group.objects.get(name="Delivery Crew")
        crew.user_set.add(user)
        return Response({"message": "Added to Delivery Crew group"}, status.HTTP_201_CREATED)

    def destroy(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        crew = Group.objects.get(name="Delivery Crew")
        crew.user_set.remove(user)
        return Response({"message": "Removed from Delivery Crew group"}, status.HTTP_201_CREATED)

        
# @api_view(["GET", "POST", "DELETE"])
# def cart(request):
#     req_method = request.method
#     if req_method == "GET":
#         a = 1

# class CartViewSet(viewsets.ModelViewSet):
#     #queryset = Cart.objects.all()
#     serializer_class = CartSerializer
    
#     def get_queryset(self):
#         #print(self.request.user.id) 
#         return Cart.objects.all().filter(user_id=self.request.user.id)
    
#     def destroy(self, request, pk=None, *args, **kwargs):
#         #a = 1
#         user_id = self.request.user.id
#         cart_items = Cart.objects.filter(user_id=user_id)
#         if cart_items:
#             cart_items.delete()
#             return Response({"messsage:ok"}, status.HTTP_200_OK)
#         #print(user_id)

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    
    def get_queryset(self):
        #print(self.request.user.id) 
        return Cart.objects.all().filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=self.request.user)
        cart_items.delete()
        return Response({"message": "cart deleted"}, status.HTTP_200_OK)
        

class OrdersView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderSerializer  
    
    def get_queryset(self):
        user_groups = self.request.user.groups
        
        if user_groups.filter(name="Delivery Crew"):
            return Order.objects.filter(delivery_crew=self.request.filter)
        elif user_groups.filter(name="Manager") or self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        cart_items_count = Cart.objects.all().filter(user=self.request.user).count()
        if cart_items_count == 0:
            return Response({"message": "no items in cart"}, status.HTTP_200_OK)
        
        req_data = request.data.copy()
        total_bill = self.get_total_bill(self.request.user)
        data["total"] = total_bill
        data["user"] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            
            cart_items = Cart.objects.all().filter(user=self.request.user)
            
            for item in cart_items.values():
                order_item = OrderItem(
                    order=order,
                    menuitem_id = item["menuitem_id"],
                    price = item["price"],
                    quantity = item["quantity"]
                )
                order_item.save()
                
            Cart.objects.all().filter(user=self.request.user).delete()
            
            result = order_serializer.data.copy()
            result["total"] = total_bill
            return Response(order_serializer.data)
        
    def get_total_bill(self, user):
        total = 0
        cart_items = Cart.objects.all().filter(user=user)
        for item in cart_items.values():
            total += item["price"]
        return total
        
# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
    
#     def get_queryset(self, **kwargs):
#         order_id = self.kwargs['id']
#         return OrderItem.objects.all().filter(order_id=order_id)
    
class SingleOrderView(generics.RetrieveUpdateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_permissions(self):
        method = self.request.method
        if method in ["DELETE"]:
            self.permission_classes = [IsAuthenticated, IsManager]
        return super().get_permissions()  
    
    def update(self, request, *args, **kwargs):
        if (self.request.user.groups.count()==0):
            return Response({"message": "Not authorized"}, status.HTTP_401_UNAUTHORIZED)    
        else:
            return super().update(request, *args, **kwargs)