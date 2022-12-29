from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator

from artworks.models import Title, Review, Comment
from django.shortcuts import get_object_or_404


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'rating', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        title = get_object_or_404(Title, id=self.context.get('title_id'))
        author = self.context['request'].user
        if Review.objects.filter(
                title_id=title,
                author_id=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение!')
        return attrs

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
