from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ForumThread, Post

User = get_user_model()

class ForumModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.thread = ForumThread.objects.create(title="Test thread", slug="test-thread", created_by=self.user)

    def test_thread_str(self):
        self.assertEqual(str(self.thread), "Test thread")

    def test_post_create(self):
        post = Post.objects.create(thread=self.thread, author=self.user, content="Hello world")
        self.assertEqual(str(post), f"{self.user} → {self.thread}")

class ForumViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='pass')
        self.moderator = User.objects.create_user(username='mod', password='pass', is_staff=True)
        self.thread = ForumThread.objects.create(title="View thread", slug="view-thread", created_by=self.moderator)

    def test_thread_list_view(self):
        url = reverse('forum:thread_list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "View thread")

    def test_thread_detail_view(self):
        url = reverse('forum:thread_detail', kwargs={'slug': self.thread.slug})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.thread.title)

    def test_create_post_requires_login(self):
        url = reverse('forum:create_post', kwargs={'thread_slug': self.thread.slug})
        res = self.client.post(url, {'content': 'Anonymous post'})
        # redirect to login (since LOGIN_URL points to /admin/login/ in our settings), so 302
        self.assertEqual(res.status_code, 302)

    def test_moderator_can_create_thread(self):
        self.client.login(username='mod', password='pass')
        url = reverse('forum:create_thread')
        res = self.client.post(url, {'title': 'New thread', 'slug': 'new-thread', 'description': 'desc'})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(ForumThread.objects.filter(slug='new-thread').exists())

    def test_non_moderator_cannot_create_thread(self):
        self.client.login(username='viewer', password='pass')
        url = reverse('forum:create_thread')
        res = self.client.get(url)
        # user_passes_test returns 302 to login by default (or 403 if configured). Check redirect.
        self.assertIn(res.status_code, (302, 403))
