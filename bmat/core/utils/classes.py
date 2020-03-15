import ast
import datetime

from django.db.models import Count
from rest_framework.exceptions import ParseError

from core import models
from core.utils.functions import get_value_or_throw_error


class Top:
    def __init__(self, request):
        self.request = request
        self.channels = self._get_channel()
        self.start_date = self._get_start()
        self.past_date = self._get_past_date()
        self.end_date = self._get_end_date()
        self.limit = self._get_limit()

    def _get_channel(self):
        channels = get_value_or_throw_error(self.request, "channels")
        try:
            return ast.literal_eval(channels)
        except SyntaxError:
            raise ParseError("Malformated channel list!")

    def _get_start(self):
        start = get_value_or_throw_error(self.request, "start")
        try:
            return datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            raise ParseError("Malformated date!")

    def _get_past_date(self):
        return self.start_date - datetime.timedelta(days=7)

    def _get_end_date(self):
        return self.start_date + datetime.timedelta(days=7)

    def _get_limit(self):
        limit = get_value_or_throw_error(self.request, "limit")
        try:
            return int(limit)
        except ValueError:
            raise ParseError("Malformated limit!")

    def _get_plays_counter(self, start, end):
        return models.Play.objects.filter(
                channel__name__in=self.channels,
                start__gte=start,
                end__lte=end
            ).values("title")\
            .annotate(plays=Count('title'))\
            .order_by("-plays")\
            .values("title", "plays", "performer")

    def _get_items(self):
        plays = self._get_plays_counter(self.start_date, self.end_date)[:self.limit]
        past_plays = self._get_plays_counter(self.past_date, self.start_date)

        items = []
        for rank, song in enumerate(plays):
            item = TopItem(rank, song, past_plays)
            items.append(item.generate_item())

        return items

    def get_response(self):
        return self._get_items()


class TopItem:
    def __init__(self, rank, song, past_plays):
        self.rank = rank
        self.song = song
        self.past_plays = past_plays
        self.song_obj = self._get_song_obj()
        self.prev_item = self._get_prev_item()

    def _get_song_obj(self):
        return models.Song.objects.get(
            pk=self.song["title"],
            performer=self.song["performer"]
        )

    def _get_prev_item(self):
        return self.past_plays.filter(
            title=self.song["title"],
            performer=self.song["performer"]
        )

    def _get_title(self):
        return self.song_obj.title

    def _get_perfomer(self):
        return self.song_obj.performer.name

    def _get_previous_plays(self):
        return self.prev_item[0]["plays"] if self.prev_item else 0

    def _get_previous_rank(self):
        return list(self.past_plays).index(self.prev_item[0]) if self.prev_item else 0

    def generate_item(self):
        return {
            "title": self._get_title(),
            "performer": self._get_perfomer(),
            "plays": self.song["plays"],
            "previous_plays": self._get_previous_plays(),
            "rank": self.rank,
            "previous_rank": self._get_previous_rank()
        }
