from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from knowledge.models import KbKnowledge
from .models import SysUser
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from .services import get_user_activity, add_subscriber, is_developer
from rest_framework.authtoken.models import Token
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compressImage(uploadedImage):
    imageTemproary = Image.open(uploadedImage).convert('RGB')
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((200, 200))
    imageTemproaryResized.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


class GetUserDetailViewSet(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image', 'email',
                      'about', 'header_image', 'facebook_profile_link', 'instagram_profile_link',
                      'twitter_profile_link', 'external_website_link', 'linkedin_profile', 'public', 'groups')

    def get(self, request, format=None):
        serializer = self.GetUserDetailFromTokenSerializer(request.user, many=False)
        # request.user.groups
        moderator = author = False
        if request.user.groups.filter(name="Moderators").exists():
            moderator = True
        if request.user.groups.filter(name="Authors").exists():
            author = True
        response = {'user': serializer.data, 'author': author, 'moderator': moderator}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.data["delete"]:
            request.user.delete()
            response = {"message": "User Deleted Successfully"}
            return Response(response, status=status.HTTP_200_OK)


class EditUserDetailViewSet(APIView):

    def post(self, request, format=None):
        # breakpoint()
        # user : SysUser
        user = request.user
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.external_website_link = request.data['external_link']
        user.instagram_profile_link = request.data['instagram_link']
        user.linkedin_profile = request.data['linkedin_link']
        user.facebook_profile_link = request.data['facebook_link']
        user.public = request.data['public']
        user.twitter_profile_link = request.data['twitter_link']
        # user.profile = request.data['profile']
        user.about = request.data['about']
        user.save()
        return Response({"message": "changed"}, status=status.HTTP_200_OK)


class EditImageOnlyViewSet(APIView):
    class EditImageOnlySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = SysUser
            fields = ['profile']

    def post(self, request, format=None):
        # breakpoint()
        user = Token.objects.get(key=request.data['token']).user
        user.profile = compressImage(request.data['profile'])
        user.save()
        return Response({"message": "changed the image mofo"}, status=status.HTTP_200_OK)


class GetUserActivity(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, requested_type, start, end, format=None):
        result = get_user_activity(request, requested_type, start, end)
        # breakpoint()
        return Response(result, status=status.HTTP_200_OK)


class AddSubscriberViewSet(APIView):

    def post(self, request, format=None):
        result = add_subscriber(request)
        return Response(result, status=status.HTTP_200_OK)


class IsDeveloperViewSet(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # breakpoint()
        result = is_developer(request.data['passcode'], request.data['username'])
        return Response(result, status=status.HTTP_200_OK)


class IsPartOfTheGroup(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_name, format=None):
        # request.user
        # breakpoint()
        if request.user.groups.filter(name=group_name).exists():
            response = True
        else:
            response = False
        return Response(response, status=status.HTTP_200_OK)


class GetUserAuthoredArticles(APIView):
    permission_classes = (IsAuthenticated,)

    class GetUserAuthoreArticlesSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ['id', 'title', 'sys_created_on', 'sys_updated_on', 'workflow', 'article_url', 'get_category',
                      'get_knowledge_base']

    def get(self, request, sort_by, state, format=None):
        # breakpoint()

        if state == 'all':
            articles = KbKnowledge.objects.filter(author=request.user, active=True).order_by(sort_by)
            articles_count = KbKnowledge.objects.filter(author=request.user, active=True).count()
            articles_data = self.GetUserAuthoreArticlesSerializer(articles, many=True)
            response = {
                'articles': articles_data.data,
                'total_count': articles_count,
            }
        if state != 'all':
            articles = KbKnowledge.objects.filter(author=request.user, active=True, workflow=state).order_by(sort_by)
            articles_count = KbKnowledge.objects.filter(author=request.user, active=True, workflow=state).count()
            articles_data = self.GetUserAuthoreArticlesSerializer(articles, many=True)
            response = {
                'articles': articles_data.data,
                'total_count': articles_count,
            }
        return Response(response, status=status.HTTP_200_OK)


class MakeUserAuthor(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        my_group = Group.objects.get(name='Authors')
        my_group.user_set.add(request.user)
        return Response('success', status=status.HTTP_201_CREATED)


class PublicUserData(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image',
                      'about', 'header_image', 'facebook_profile_link', 'instagram_profile_link',
                      'twitter_profile_link', 'external_website_link', 'linkedin_profile', 'public', 'groups')

    def get(self, request, id, format=None):
        try:
            user = SysUser.objects.get(id_name=id, is_active=True, public=True)
        except ObjectDoesNotExist:
            return Response('', status=status.HTTP_404_NOT_FOUND)
        serializer = self.GetUserDetailFromTokenSerializer(user, many=False)
        # request.user.groups
        moderator = author = False
        if user:
            if user.groups.filter(name="Moderators").exists():
                moderator = True
            if user.groups.filter(name="Authors").exists():
                author = True
            response = {'user': serializer.data, 'author': author, 'moderator': moderator}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response('User has deactivated his account!', status=status.HTTP_404_NOT_FOUND)


class GetPublicAuthorArticles(APIView):
    class GetUserAuthoreArticlesSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ['id', 'title', 'get_knowledge_base', 'get_category', 'article_url']

    def get(self, request, id_name, sort_by, format=None):
        # breakpoint()
        try:
            user = SysUser.objects.get(id_name=id_name, public=True, is_active=True)
        except ObjectDoesNotExist:
            return Response('User has deactivated his account', status=status.HTTP_404_NOT_FOUND)
        articles = KbKnowledge.objects.filter(author=user, active=True, workflow="published").order_by(sort_by)
        articles_count = KbKnowledge.objects.filter(author=user, active=True).count()
        articles_data = self.GetUserAuthoreArticlesSerializer(articles, many=True)
        response = {
            'articles': articles_data.data,
            'total_count': articles_count,
        }
        return Response(response, status=status.HTTP_200_OK)
