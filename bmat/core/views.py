from django.core.exceptions import ValidationError
from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core import models, serializers
from core.utils.classes import Top
from core.utils.functions import get_value_or_throw_error


class CreateChannelAPIView(CreateAPIView):
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer


class CreatePerfomerAPIView(CreateAPIView):
    queryset = models.Performer.objects.all()
    serializer_class = serializers.PerformerSerializer


class CreateSongAPIView(CreateAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer


class CreatePlayAPIView(CreateAPIView):
    queryset = models.Play.objects.all()
    serializer_class = serializers.PlaySerializer


class GetSongPlaysAPIView(ModelViewSet):
    serializer_class = serializers.ChannelPlaySerializer

    def get_queryset(self):
        title = get_value_or_throw_error(self.request, "title")
        performer = get_value_or_throw_error(self.request, "performer")
        start = get_value_or_throw_error(self.request, "start")
        end = get_value_or_throw_error(self.request, "end")

        try:
            queryset = models.Play.objects.filter(
                title__title=title,
                performer__name=performer,
                start__gte=start, end__lte=end
            )
        except ValidationError:
            raise ParseError("Bad parameters!")

        return queryset


class GetChannelPlaysAPIView(ModelViewSet):
    serializer_class = serializers.SongPlaySerializer

    def get_queryset(self):
        channel = get_value_or_throw_error(self.request, "channel")
        start = get_value_or_throw_error(self.request, "start")
        end = get_value_or_throw_error(self.request, "end")

        try:
            queryset = models.Play.objects.filter(
                channel__name=channel,
                start__gte=start, end__lte=end
            )
        except ValidationError:
            raise ParseError("Bad parameters!")

        return queryset


class GetTopAPIView(APIView):
    def get(self, request):
        response = Top(request).get_response()
        return Response(response)
