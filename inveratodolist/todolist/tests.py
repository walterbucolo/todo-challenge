from django.test import RequestFactory, TestCase
from todolist.views import (
    UserDetail,
    UserList,
    UserTasksList,
    UserTasksDetail,
    UserTasksSearch,
)
from todolist.models import User, Task
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import force_authenticate
from datetime import datetime



class TestUserList(TestCase):
    def test_get_list_of_users(self):
        users = []
        for i in range(5):
            user = User(
                username = "user - {}".format(i),
                email = "user{}@gmail.com".format(i),
            )
            user.set_password("passwd")
            user.save()
            users.append(user)
        request = RequestFactory().get('/users/')

        response = UserList.as_view()(request)

        assert response.data['count'] == 5
        assert [response.data['results'][i]['id'] == users[i].id for i in range(5)]

    def test_create_user(self):
        data = {
            'username': "newuser",
            'password': "passwd",
            'email': "email@test.com",
        }
        request = RequestFactory().post('/users/', data=data)

        response = UserList.as_view()(request)

        assert response.status_code == 201

    def test_create_user_fails_when_username_is_missing(self):
        data = {
            'password': "passwd",
            'email': "email@test.com",
        }
        request = RequestFactory().post('/users/', data=data)

        response = UserList.as_view()(request)

        assert response.status_code == 400
        assert response.data['username'] == [ErrorDetail(string='This field is required.', code='required')]

    def test_create_user_fails_when_password_is_missing(self):
        data = {
            'username': "newuser",
            'email': "email@test.com",
        }
        request = RequestFactory().post('/users/', data=data)

        response = UserList.as_view()(request)

        assert response.status_code == 400
        assert response.data['password'] == [ErrorDetail(string='This field is required.', code='required')]


class TestUserDetail(TestCase):
    def setUp(self) -> None:
        self.user = User(
            username = "username",
            email = "username@gmail.com",
        )
        self.user.set_password("passwd")
        self.user.save()


    def test_retrieve_user(self):
        request = RequestFactory().get('/users/{pk}'.format(pk=self.user.id))
        force_authenticate(request, user=self.user)

        response = UserDetail.as_view()(request, pk=self.user.id)

        assert response.status_code == 200
        assert response.data['id'] == self.user.id

    def test_update_user(self):
        data = {'username': "changedusername"}
        request = RequestFactory().put('/users/{}'.format(self.user.id), data=data, content_type='application/json')
        force_authenticate(request, user=self.user)

        response = UserDetail.as_view()(request, pk=self.user.id)

        assert response.status_code == 200

    def test_delete_user(self):
        request = RequestFactory().delete('/users/{}'.format(self.user.id))
        force_authenticate(request, user=self.user)

        response = UserDetail.as_view()(request, pk=self.user.id)

        assert response.status_code == 204

class TestUserTasksList(TestCase):
    def setUp(self) -> None:
        self.user = User(username="username", email="email@test.com")
        self.user.set_password("passwd")
        self.user.save()

    def test_get_list_of_user_tasks(self):
        tasks = []
        for i in range(5):
            task = Task.objects.create(
                title = "Doctor appointment {}".format(i),
                description = "Ask for painkillers",
                date = datetime.now(),
                user = self.user,
            )
            tasks.append(task)
        request = RequestFactory().get('/users/{}/tasks'.format(self.user.id))
        force_authenticate(request, user=self.user)


        response = UserTasksList.as_view()(request, pk=self.user.id)

        assert response.data['count'] == 5
        assert [response.data['results'][i]['id'] == tasks[i].id for i in range(5)]

    def test_create_user_task(self):
        data = {
            'title': "Football match",
            'description': "With friends",
            'date': datetime.now(),
        }
        request = RequestFactory().post('/users/{}/tasks'.format(self.user.id), data=data)
        force_authenticate(request, user=self.user)


        response = UserTasksList.as_view()(request, pk=self.user.id)

        assert response.status_code == 201

    def test_create_user_task_fail_when_user_is_not_authenticated(self):
        data = {
            'title': "Football match",
            'description': "With friends",
            'date': datetime.now(),
        }
        request = RequestFactory().post('/users/{}/tasks'.format(self.user.id), data=data)

        response = UserTasksList.as_view()(request, pk=self.user.id)

        assert response.status_code == 401
    
    def test_create_user_task_fail_when_user_is_not_authorized(self):
        data = {
            'title': "Football match",
            'description': "With friends",
            'date': datetime.now(),
        }
        request = RequestFactory().post('/users/{}/tasks'.format(self.user.id), data=data)
        user_fake = User.objects.create(username="anotheruser")
        force_authenticate(request, user=user_fake)

        response = UserTasksList.as_view()(request, pk=self.user.id)

        assert response.status_code == 403

class TestUserTasksDetail(TestCase):
   
    def setUp(self) -> None:
        self.user = User(
            username = "username",
            email = "username@gmail.com",
        )
        self.user.set_password("passwd")
        self.user.save()
        self.task = Task.objects.create(title="Call mom", description="ask something", date=datetime.now(), user=self.user)

    def test_retrieve_task(self):
        request = RequestFactory().get('/users/{pk}/tasks/{id}'.format(pk=self.task.user.id, id=self.task.id))
        force_authenticate(request, user=self.user)

        response = UserTasksDetail.as_view()(request, pk=self.task.user.id, id=self.task.id)

        assert response.status_code == 200
        assert response.data['id'] == self.task.id

    def test_retrieve_task_fails_when_user_is_not_authorized(self):
        fake_user = User.objects.create(username="something", email="email@test.com")
        request = RequestFactory().get('/users/{pk}/tasks/{id}'.format(pk=self.task.user.id, id=self.task.id))
        force_authenticate(request, user=fake_user)

        response = UserTasksDetail.as_view()(request, pk=self.task.user.id, id=self.task.id)

        assert response.status_code == 403

    def test_update_task(self):
        data = {'status': 2}
        request = RequestFactory().patch(
            '/users/{pk}/tasks/{id}'.format(pk=self.task.user.id, id=self.task.id),
            data=data,
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)

        response = UserTasksDetail.as_view()(request, pk=self.task.user.id, id=self.task.id)

        assert response.status_code == 200

    def test_delete_task(self):
        request = RequestFactory().delete('/users/{pk}/tasks/{id}'.format(pk=self.task.user.id, id=self.task.id))
        force_authenticate(request, user=self.user)

        response = UserTasksDetail.as_view()(request, pk=self.task.user.id, id=self.task.id)

        assert response.status_code == 204

class TestUserTasksSearch(TestCase):
    def setUp(self) -> None:
        self.user = User(username="username", email="email@test.com")
        self.user.set_password("passwd")
        self.user.save()

    def test_search_list_of_user_tasks_by_title(self):
        task = Task.objects.create(
            title = "Doctor appointment",
            description = "Ask for painkillers",
            date = datetime.now(),
            user = self.user,
        )
        Task.objects.create(
            title = "Buy clothe",
            description = "In the shop",
            date = datetime.now(),
            user = self.user,
        )
        query_title = 'Doctor ap'
        request = RequestFactory().get('/users/{}/tasks/search?title={}'.format(self.user.id, query_title))
        force_authenticate(request, user=self.user)


        response = UserTasksSearch.as_view()(request, pk=self.user.id)

        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == task.id

    def test_search_list_of_user_tasks_by_date(self):
        Task.objects.create(
            title = "Doctor appointment",
            description = "Ask for painkillers",
            date = datetime(2022, 1, 1, 8, 14),
            user = self.user,
        )
        task_two = Task.objects.create(
            title = "Buy clothe",
            description = "In the shop",
            date = datetime(2022, 2, 1, 8, 14),
            user = self.user,
        )
        query_date = '2022-02-01T08:14'
        request = RequestFactory().get('/users/{}/tasks/search?date={}'.format(self.user.id, query_date))
        force_authenticate(request, user=self.user)


        response = UserTasksSearch.as_view()(request, pk=self.user.id)
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == task_two.id