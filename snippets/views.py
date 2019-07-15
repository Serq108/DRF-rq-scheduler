from django.shortcuts import render



from snippets.models import Snippet, CourseList, CoursePage, CourseUsers
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer, UserSerializer,\
    UserCreateSerializer, CreateSnippetSerializer, CreateCourseSerializer,\
    CreateCoursePageSerializer, CourseDetailSerializer, CourseListSerializer,\
    CoursePageSerializer, CourseDetailPageSerializer, CourseUserSerializer,\
    CourseUsersListSerializer, CourseUserDetailSerializer

from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly, IfGroup2

from utils.token_generator import token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers

class SnippetList(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CreateSnippet(generics.CreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = CreateSnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = CreateSnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly, IfGroup2)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer


class CreateCourseView(generics.ListCreateAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CreateCourseSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreatePageView(generics.ListCreateAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CreateCoursePageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursListView(generics.ListAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly,)


class CoursPageListView(generics.ListAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CoursePageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CourseDetailPageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursUserView(generics.CreateAPIView):
    queryset = CourseUsers.objects.all()
    serializer_class = CourseUserSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CoursUserListView(generics.ListAPIView):
    queryset = CourseUsers.objects.all()
    serializer_class = CourseUsersListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseUsers.objects.all()
    serializer_class = CourseUserDetailSerializer
    permission_classes = (permissions.DjangoModelPermissions,  IsOwnerOrReadOnly,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'users': reverse('user-list', request=request, format=format),
        # 'snippets': reverse('snippet-list', request=request, format=format),
        'courses': reverse('courselist-list', request=request, format=format),
        'registration': reverse('user-list', request=request, format=format)
    })


class ConfirmEmailView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request, user, token):
        try:
            uid = force_text(urlsafe_base64_decode(user))
            user = get_user_model().objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # ~ return Response(data={'status': 'ok'}, content_type='application/json', status=status.HTTP_202_ACCEPTED)
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'error', 'message': 'Неверная ссылка активации'})
                # ~ status=status.HTTP_400_BAD_REQUEST
        

    # ~ class SnippetHighlight(generics.GenericAPIView):
    # ~ queryset = Snippet.objects.all()
    # ~ renderer_classes = (renderers.StaticHTMLRenderer,)

    # ~ def get(self, request, *args, **kwargs):
        # ~ snippet = self.get_object()
        # ~ return Response(snippet.highlighted)
