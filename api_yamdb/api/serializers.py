from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from artworks.models import Title, Review, Comment

class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'rating', 'created_at')


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username'
#     )
#     title = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Review
#         fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
        # default=serializers.CreateOnlyDefault()
        # default=serializers.SerializerMethodField('get_title')
    )
    # title = self.context['title']
    # title = self.context.get('title')

    # def __call__(self, value, serializer_field):
    #     title = self.context.get('title')

    # def save(self):
    #     author = CurrentUserDefault()  # <= magic!
    #     title = self.validated_data['title']

    # def get_title(self):
    #     title_id = self.context['title']
    #     title = Title.objects.get(title_id)
    #     return title

    # class Meta:
    #     model = Review
    #     fields = ('title', 'author')
    #     validators = [
    #         UniqueTogetherValidator(
    #             queryset=Review.objects.all(),
    #             fields=('title', 'author'),
    #             message='Вы уже оставили отзыв на данное произведение!'
    #         )
    #     ]

    # def get_title(self):
    #     title = self.context.get['title']
    #     return title

    def validate(self, attrs):
        title_id = self.context['request'].title_id
        author = self.context['request'].user
        if Review.objects.filter(
                title_id=title_id,
                author_id=author.id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение!')

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
