from rest_framework import serializers
from django.shortcuts import get_object_or_404

from artworks.models import Title, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'rating', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        title = get_object_or_404(
            Title,
            id=self.context['view'].kwargs.get('title_id'))
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    title_id=title, author_id=author).exists():
                raise serializers.ValidationError(
                    'You have already left a review for this title!')
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
