from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='ТЕСТТекст',
            pub_date='29.11.2077',
            author=User.objects.create(
                first_name='Чернее',
                last_name='Куковского'
            ),
            group=Group.objects.create(
                slug='writers',
                description='ТЕСТОписание',
                title='ТЕСТПисатели',
            ),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Shootka..')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/writers/',
            'posts/post_detail.html': 'posts/1/',
            'posts/profile.html': 'profile/Shootka../',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_test_urls_uses_correct_template_auth(self):
        response = self.authorized_client.get('create/')
        template = 'posts/create_post.html'
        self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        response = self.guest_client.get('unexisting_page/')
        self.assertEqual(response.status_code, 404)
