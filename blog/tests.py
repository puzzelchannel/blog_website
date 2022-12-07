from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from .models import Post


# Create your tests here.

class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testing_user')
        cls.published_testing_post = Post.objects.create(
            title='testing published post',
            text='this is a testing published post',
            status='pub',
            author=cls.user,
        )

        cls.draft_testing_post = Post.objects.create(
            title='testing draft post',
            text='this is a testing draft post',
            status='drf',
            author=cls.user,
        )

    def test_post_list_by_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(200, response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(200, response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.published_testing_post.title)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.published_testing_post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.published_testing_post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_blog_detail_page(self):
        response = self.client.get(f'/blog/{self.published_testing_post.id}/')
        self.assertContains(response, self.published_testing_post.title)
        self.assertContains(response, self.published_testing_post.text)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_posts_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.published_testing_post.title)
        self.assertNotContains(response, self.draft_testing_post.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Some Title',
            'text': 'Some Text',
            'status': 'pub',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title')
        self.assertEqual(Post.objects.last().text, 'Some Text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.draft_testing_post.id]), {
            'title': 'Some Title Update',
            'text': 'Some Text Update',
            'status': 'pub',
            'author': self.draft_testing_post.author.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title Update')
        self.assertEqual(Post.objects.last().text, 'Some Text Update')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.draft_testing_post.id]), )
        self.assertEqual(response.status_code, 302)
