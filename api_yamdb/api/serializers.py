from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator

from artworks.models import Title, Review, Comment


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'description', 'rating', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='username',
#         default=serializers.CurrentUserDefault()
#     )
#     title = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Review
#         fields = ('title', 'author')
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Review.objects.all(),
#                 fields=('title', 'author'),
#                 message='Вы уже оставили отзыв на данное произведение!'
#             )
#         ]


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
