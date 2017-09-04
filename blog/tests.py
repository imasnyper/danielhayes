from .models import Post
from django.urls import reverse
from django.utils import timezone
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
import random


def create_post(user, post_text, days):
    """
    Create a question with the given 'post_text' and published the given number
    of 'days' offset to now (negative for posts published in the past, positive
    for posts that have yet to be published.
    :param user: user who created the post
    :param post_text: text of created post
    :param days: number of days offset from now
    :return: post with options
    """

    time = timezone.now() + datetime.timedelta(days=days)
    slug = random.randint(1, 1000000)
    return Post.objects.create(author=user, title=post_text,
                               slug=slug, pub_date=time)


class PostIndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test daniel',
            email='test@test.com',
            password='dontlook'
        )

    def test_no_posts(self):
        """
        If no posts exist, an appropriate message is displayed
        :return:
        """

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_past_post(self):
        """
        Posts with a pub_date in the past are displayed on the index page.
        :return:
        """

        create_post(user=self.user, post_text="Past post.", days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['posts'], ['<Post: Past post.>']
        )

    def test_future_post(self):
        """
        Question with a pub_date in the future aren't displayed on the index
        page.
        :return:
        """
        create_post(user=self.user, post_text="Future post.", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_future_post_and_past_post(self):
        """
        Even if both past and future questions exist, only past questions are
        displayed.
        :return:
        """
        create_post(user=self.user, post_text="Past post.", days=-30)
        create_post(user=self.user, post_text="Future post.", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['posts'], ['<Post: Past post.>'])

    def test_two_past_posts(self):
        """
        The blog index page may display multiple posts
        :return:
        """
        create_post(user=self.user, post_text="Past post 1.", days=-30)
        create_post(user=self.user, post_text="Past post 2.", days=-5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>'])