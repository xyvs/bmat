from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from rest_framework import serializers

from core import models


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        channel, _ = models.Channel.objects.get_or_create(**validated_data)
        return channel


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Performer
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        performer, _ = models.Performer.objects.get_or_create(**validated_data)
        return performer


class SongSerializer(serializers.ModelSerializer):
    performer = CreatableSlugRelatedField(
        queryset=models.Performer.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Song
        fields = ['title', 'performer']

    def create(self, validated_data):
        song, _ = models.Song.objects.get_or_create(**validated_data)
        return song


class PlaySerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        queryset=models.Song.objects.all(),
        slug_field='title'
    )
    performer = serializers.SlugRelatedField(
        queryset=models.Performer.objects.all(),
        slug_field='name'
    )
    channel = serializers.SlugRelatedField(
        queryset=models.Channel.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Play
        fields = ['title', 'performer', 'channel', 'start', 'end']

    def create(self, validated_data):
        play, _ = models.Play.objects.get_or_create(**validated_data)
        return play


class ChannelPlaySerializer(serializers.ModelSerializer):

    channel = serializers.SlugRelatedField(
        queryset=models.Channel.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Play
        fields = ['channel', 'start', 'end']


class SongPlaySerializer(serializers.ModelSerializer):

    title = serializers.SlugRelatedField(
        queryset=models.Song.objects.all(),
        slug_field='title'
    )
    performer = serializers.SlugRelatedField(
        queryset=models.Performer.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Play
        fields = ['title', 'performer', 'start', 'end']
