from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . models import Account, Video


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pmvc:user-detail")
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pmvc:group-detail")
    class Meta:
        model = Group
        fields = ['url', 'name']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pmvc:account-detail")
    class Meta:
        model = Account
        fields = ['url', 'name', 'enabled']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pmvc:video-detail")
    class Meta:
        model = Video
        fields = ['url', 'id', 'title', 'description']