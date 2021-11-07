from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='ТЕСТЗаголовок',
            slug='skip',
            description='ТЕСТОписание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='улитка и бар',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        field_str = {
            post: post.text,
            group: group.title,
        }
        for field, expected_value in field_str.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value, str(field),
                )
