from rest_framework import serializers
from .models import Category, Errand, ErrandApplication, Review, Cancellation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ErrandSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)
    tasker_username = serializers.CharField(source='tasker.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Errand
        fields = ['id', 'title', 'description', 'client', 'client_username', 'tasker', 'tasker_username', 
                 'category', 'category_name', 'location', 'preferred_date', 'preferred_time', 'budget', 
                 'status', 'created_at', 'updated_at']
        read_only_fields = ('client', 'tasker', 'status')

class ErrandApplicationSerializer(serializers.ModelSerializer):
    tasker_username = serializers.CharField(source='tasker.username', read_only=True)
    errand_title = serializers.CharField(source='errand.title', read_only=True)
    
    class Meta:
        model = ErrandApplication
        fields = '__all__'
        read_only_fields = ('tasker', 'status')

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    reviewed_username = serializers.CharField(source='reviewed.username', read_only=True)
    errand_title = serializers.CharField(source='errand.title', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer',)

class CancellationSerializer(serializers.ModelSerializer):
    errand_title = serializers.CharField(source='errand.title', read_only=True)
    cancelled_by_username = serializers.CharField(source='cancelled_by.username', read_only=True)
    
    class Meta:
        model = Cancellation
        fields = '__all__'
        read_only_fields = ('cancelled_by', 'cancelled_at', 'refund_status', 'refund_amount', 'refund_transaction_id') 