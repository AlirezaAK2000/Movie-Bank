from .models import (
    Movie,
    Comment,
    Vote
)

from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()    
    id = serializers.ReadOnlyField(source='pk')
    class Meta:
        model = Movie
        fields = ['name' , 'description' , 'rating' , 'id']

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    user = serializers.ReadOnlyField(source="user.pk")
    class Meta:
        model = Comment
        fields = '__all__'
        
    def create(self, validated_data):
        comment = Comment.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return comment

class VoteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    user = serializers.ReadOnlyField(source="user.pk")
    
    class Meta:
        model = Vote
        fields = '__all__'
    
    def create(self, validated_data):
        vote = Vote.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return vote


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    author = serializers.ReadOnlyField(source="user.pk")
    body = serializers.ReadOnlyField(source="comment_body")
    
    class Meta:
        model = Comment
        fields = ['id' , 'author' , 'body']