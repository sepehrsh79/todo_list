import datetime

import factory

from django.utils import timezone

from todo_list.tests.utils import faker
from todo_list.users.models import BaseUser, Profile
from todo_list.todo.models import Task, Board, Group


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    email = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.LazyAttribute(lambda _: faker.unique.company())
    user = factory.SubFactory(BaseUserFactory)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    description = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    group = factory.SubFactory(GroupFactory)
    user = factory.SubFactory(BaseUserFactory)
    created_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')

    @factory.post_generation
    def permitted_users(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.permitted_users.add(*extracted)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    description = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(BaseUserFactory)
    completed = factory.LazyAttribute(lambda _: faker.boolean(chance_of_getting_true=50))
    deadline = factory.LazyAttribute(lambda _: f'{timezone.now().date() + datetime.timedelta(days=10)}')
    created_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')

    @factory.post_generation
    def permitted_users(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.permitted_users.add(*extracted)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(BaseUserFactory)
    bio = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
