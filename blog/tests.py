from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from .models import Post


# Create your tests here.

class BlogPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testing_user')
        self.published_testing_post = Post.objects.create(
            title='testing published post',
            text='this is a testing published post',
            status=Post.STATUS_CHOICES[0][0],
            author=self.user
        )

        self.draft_testing_post = Post.objects.create(
            title='testing draft post',
            text='this is a testing draft post',
            status=Post.STATUS_CHOICES[1][0],
            author=self.user
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
        response = self.client.get(reverse('posts_detail', args=[self.published_testing_post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_blog_detail_page(self):
        response = self.client.get(f'/blog/{self.published_testing_post.id}/')
        self.assertContains(response, self.published_testing_post.title)
        self.assertContains(response, self.published_testing_post.text)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('posts_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_posts_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.published_testing_post.title)
        self.assertNotContains(response, self.draft_testing_post.title)
