from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from core.models import User
from goals.models import GoalCategory, Goal, Board, BoardParticipant


class GoalCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('goal-create')
        self.user = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.board = Board.objects.create(
            title='test_board_title'
        )
        self.board_participant = BoardParticipant.objects.create(
            board=self.board,
            user=self.user,
            role=BoardParticipant.Role.owner.value
        )
        self.category = GoalCategory.objects.create(
            title='test_goal_category_title',
            user=self.user,
            board=self.board
        )

    def test_goal_create_success(self):
        self.client.force_login(self.user)
        now = timezone.now()
        response = self.client.post(
            path=self.url,
            data={
                'title': 'new_test_goal',
                'category': self.category.id,
                'due_date': now
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        goal = Goal.objects.last()

        self.assertDictEqual(
            response.json(),
            {
                'id': goal.id,
                'title': 'new_test_goal',
                'description': None,
                'category': self.category.id,
                'status': Goal.Status.to_do.value,
                'priority': Goal.Priority.medium.value,
                'due_date': timezone.localtime(now).isoformat(),
                'created': timezone.localtime(goal.created).isoformat(),
                'updated': timezone.localtime(goal.updated).isoformat()
            }
        )

    def test_not_board_owner(self):
        user_2 = User.objects.create(
            username='test_user2',
            password='test_password2'
        )
        self.client.force_login(user=user_2)
        now = timezone.now()
        response = self.client.post(
            path=self.url,
            data={
                'title': 'new_test_goal',
                'category': self.category.id,
                'due_date': now
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OneGoalTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.board = Board.objects.create(
            title='test_board_title'
        )
        self.board_participant = BoardParticipant.objects.create(
            board=self.board,
            user=self.user,
            role=BoardParticipant.Role.owner.value
        )
        self.category = GoalCategory.objects.create(
            title='test_goal_category_title',
            user=self.user,
            board=self.board
        )
        now = timezone.now()
        self.goal = Goal.objects.create(
            title='test_goal',
            category=self.category,
            due_date=now,
            user=self.user,
            created=now,
            updated=now
        )
        self.url = reverse('goal-one', kwargs={'pk': self.goal.pk})

    def test_retrieve_goal(self):
        self.client.force_login(self.user)
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.goal.id,
                'title': 'test_goal',
                'description': None,
                'category': self.category.id,
                'status': Goal.Status.to_do.value,
                'priority': Goal.Priority.medium.value,
                'due_date': timezone.localtime(self.goal.due_date).isoformat(),
                'created': timezone.localtime(self.goal.created).isoformat(),
                'updated': timezone.localtime(self.goal.updated).isoformat(),
                'user': self.user.id
            }
        )

    def test_update_goal(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            path=self.url,
            data={
                'description': 'test_description'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.goal.refresh_from_db(fields=['description'])
        self.assertEqual(self.goal.description, 'test_description')

    def test_goal_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Goal.objects.first().status, Goal.Status.archived)

    def test_failure(self):
        self.assertTrue(False, 'failure')
