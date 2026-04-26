from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from posts.models import Post, Comment
from friends.models import Follow, FriendRequest


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass1234')

    def test_profile_auto_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(str(self.user.profile), 'alice Profile')

    def test_profile_counts_start_at_zero(self):
        self.assertEqual(self.user.profile.get_posts_count(), 0)
        self.assertEqual(self.user.profile.get_followers_count(), 0)


class PostModelTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob   = User.objects.create_user(username='bob',   password='pass1234')
        self.post  = Post.objects.create(author=self.alice, content='Hello world')

    def test_like_count(self):
        self.assertEqual(self.post.like_count(), 0)
        self.post.likes.add(self.bob)
        self.assertEqual(self.post.like_count(), 1)

    def test_is_liked_by(self):
        self.assertFalse(self.post.is_liked_by(self.bob))
        self.post.likes.add(self.bob)
        self.assertTrue(self.post.is_liked_by(self.bob))

    def test_comment_count(self):
        Comment.objects.create(post=self.post, author=self.bob, content='Nice!')
        self.assertEqual(self.post.comment_count(), 1)

    def test_ordering_newest_first(self):
        post2 = Post.objects.create(author=self.alice, content='Second')
        self.assertEqual(Post.objects.first(), post2)


class FollowTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob   = User.objects.create_user(username='bob',   password='pass1234')

    def test_follow(self):
        Follow.objects.create(follower=self.alice, following=self.bob)
        self.assertEqual(self.bob.followers.count(), 1)

    def test_follow_unique(self):
        Follow.objects.create(follower=self.alice, following=self.bob)
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.alice, following=self.bob)


class FeedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob   = User.objects.create_user(username='bob',   password='pass1234')
        self.client.login(username='alice', password='pass1234')

    def test_feed_shows_own_posts(self):
        Post.objects.create(author=self.alice, content='My post')
        resp = self.client.get(reverse('feed'))
        self.assertContains(resp, 'My post')

    def test_feed_shows_followed_posts(self):
        Follow.objects.create(follower=self.alice, following=self.bob)
        Post.objects.create(author=self.bob, content="Bob's post")
        resp = self.client.get(reverse('feed'))
        self.assertContains(resp, "Bob's post")

    def test_feed_hides_unfollowed_posts(self):
        Post.objects.create(author=self.bob, content='Hidden')
        resp = self.client.get(reverse('feed'))
        self.assertNotContains(resp, 'Hidden')

    def test_feed_redirects_anonymous(self):
        self.client.logout()
        resp = self.client.get(reverse('feed'))
        self.assertEqual(resp.status_code, 302)