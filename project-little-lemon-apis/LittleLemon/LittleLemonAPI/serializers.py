from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import Group, User


class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        #fields = ['id', 'title', 'price', 'featured']
        depth = 1
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
        
class CartSerializer(serializers.ModelSerializer):
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    
    class Meta:
        model = Cart
        fields = ["id", "menuitem", "menuitem_id", "quantity", "unit_price", "price"]

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ["order", "menuitem", "quantity", "unit_price", "price"]
 
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order", "menuitem", "quantity", "unit_price", "price"]
        
# class OrderSerializer(serializers.ModelSerializer):
#     #user = UserSerializer()
#     #delivery_crew = UserSerializer()
#     orderitem = OrderItemSerializer(many=True, read_only=True, source="order")
#     #orderItem_id = serializers.IntegerField()
    
#     class Meta:
#         model = Order
#         fields = ["id", "user", "orderitem"]
#         #fields = "__all__"
#         #depth = 1
        
class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True, source="order")

    class Meta:
        model = Order
        fields = ["id", "user", "delivery_crew", "status", "date", "total", "orderitem"]