import datetime
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Channel, Performer, Play, Song


class ChannelTests(APITestCase):

    def _generate_response(self, data):
        request_url = reverse('add_channel')
        return self.client.post(request_url, data, format='json')

    def _generate_empty_response(self):
        return self._generate_response({})

    def _generate_normal_response(self):
        return self._generate_response({'name': 'KBS'})

    def test_error_reponse_with_no_data(self):
        response = self._generate_empty_response()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_channel(self):
        response = self._generate_normal_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Channel.objects.first().name, 'KBS')

    def test_create_channel_that_already_exists(self):
        response_first_time = self._generate_normal_response()
        response_second_time = self._generate_normal_response()
        self.assertEqual(response_first_time.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second_time.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Channel.objects.count(), 1)


class PerformerTests(APITestCase):

    def _generate_response(self, data):
        request_url = reverse('add_performer')
        return self.client.post(request_url, data, format='json')

    def _generate_empty_response(self):
        return self._generate_response({})

    def _generate_normal_response(self):
        return self._generate_response({'name': 'The Smiths'})

    def test_error_reponse_with_no_data(self):
        response = self._generate_empty_response()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_channel(self):
        response = self._generate_normal_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performer.objects.count(), 1)
        self.assertEqual(Performer.objects.first().name, 'The Smiths')

    def test_create_performer_that_already_exists(self):
        response_first_time = self._generate_normal_response()
        response_second_time = self._generate_normal_response()
        self.assertEqual(response_first_time.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second_time.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performer.objects.count(), 1)


class SongTests(APITestCase):

    def setUp(self):
        Performer.objects.create(name="Pixies")

    def _generate_response(self, data):
        url = reverse('add_song')
        return self.client.post(url, data, format='json')

    def test_create_song_with_performer_that_does_exists(self):
        response = self._generate_response({'title': 'Gouge Away', 'performer': 'Pixies'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Performer.objects.count(), 1)

    def test_create_song_with_performer_that_doesnt_exists(self):
        response = self._generate_response({'title': 'Brother Sport', 'performer': 'Animal Collective'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)


class PlayTests(APITestCase):

    def setUp(self):

        channel = Channel.objects.create(name="Punk-rock 101.2")
        performer = Performer.objects.create(name="blink-182")
        song = Song.objects.create(title="I Miss You", performer=performer)

        self.data = {
            "title": song.title,
            "performer": performer.name,
            "channel": channel.name,
            "start": "2014-10-21T00:00:00",
            "end": "2014-10-28T00:00:00",
        }

    def _generate_response(self):
        url = reverse('add_play')
        return self.client.post(url, self.data, format='json')

    def test_create_play(self):
        response = self._generate_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 1)

    def test_create_play_twice(self):
        first_play_response = self._generate_response()
        second_play_response = self._generate_response()
        self.assertEqual(first_play_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_play_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 1)


class GetValues(APITestCase):

    def _create_song(self, title, performer):
        performer, _ = Performer.objects.get_or_create(name=performer)
        song = Song.objects.create(title=title, performer=performer)
        return song

    def _create_play(self, title, channel, start):
        start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end = start + datetime.timedelta(seconds=300)
        play = Play.objects.create(
            title=title,
            performer=title.performer,
            channel=channel,
            start=start,
            end=end
        )
        return play

    def _generate_response(self, url, data):
        return self.client.get(reverse(url), data, format='json')

    def setUp(self):
        self.song1 = self._create_song("Eclipse", "이달의 소녀")
        self.song2 = self._create_song("Piccadilly Palare", "Morrisey")
        self.song3 = self._create_song("Safaera", "Bad Bunny")

        self.channel1 = Channel.objects.create(name="KBS")
        self.channel2 = Channel.objects.create(name="International Radio")

        self._create_play(self.song1, self.channel1, "2020-01-01T00:00:00")
        self._create_play(self.song3, self.channel1, "2020-01-03T00:00:00")
        self._create_play(self.song1, self.channel1, "2020-01-05T00:00:00")
        self._create_play(self.song1, self.channel1, "2020-01-07T00:00:00")
        self._create_play(self.song2, self.channel1, "2020-01-09T00:00:00")

        self._create_play(self.song2, self.channel2, "2020-01-01T00:00:00")
        self._create_play(self.song3, self.channel2, "2020-01-03T00:00:00")
        self._create_play(self.song3, self.channel2, "2020-01-05T00:00:00")
        self._create_play(self.song2, self.channel2, "2020-01-07T00:00:00")
        self._create_play(self.song1, self.channel2, "2020-01-09T00:00:00")

    def test_song_plays_with_no_data(self):
        response = self._generate_response('get_song_plays', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_song_plays_with_malformated_data(self):
        data = {
            "title": self.song1.title,
            "performer": self.song1.performer.name,
            "start": "01-01-2020",
            "end": "05-01-2020",

        }
        response = self._generate_response('get_song_plays', data)
        self.assertEqual(json.loads(response.content), {'detail': 'Bad parameters!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_song_plays_with_formated_data(self):
        data = {
            "title": self.song3.title,
            "performer": self.song3.performer.name,
            "start": "2020-01-01",
            "end": "2020-01-05",

        }
        response = self._generate_response('get_song_plays', data)
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_channel_plays_with_no_data(self):
        response = self._generate_response('get_channel_plays', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_channel_plays_with_malformated_data(self):
        data = {
            "channel": self.channel1.name,
            "start": "01-01-2020",
            "end": "05-01-2020",

        }
        response = self._generate_response('get_channel_plays', data)
        self.assertEqual(json.loads(response.content), {'detail': 'Bad parameters!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_channel_plays_with_formated_data(self):
        data = {
            "channel": self.channel1.name,
            "start": "2020-01-01",
            "end": "2020-01-05",

        }
        response = self._generate_response('get_channel_plays', data)
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_with_no_data(self):
        response = self._generate_response('get_top', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _get_top_data(self, channel, start, limit):
        return {"channels": channel, "start": start, "limit": limit}

    def _test_top_malformatted(self, values, error):
        data = self._get_top_data(*values)
        response = self._generate_response('get_top', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'detail': error})

    def _test_top_success(self, values, length):
        data = self._get_top_data(*values)
        response = self._generate_response('get_top', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), length)

    def test_top_with_malformated_list(self):
        self._test_top_malformatted(
            values=('KBS, International Radio',  "2020-01-01T00:00:00", 3),
            error='Malformated channel list!'
        )

    def test_top_with_malformated_date(self):
        self._test_top_malformatted(
            values=('["KBS", "International Radio"]', "Today", 3),
            error='Malformated date!'
        )

    def test_top_with_malformated_limit(self):
        self._test_top_malformatted(
            values=('["KBS", "International Radio"]', "2020-01-01T00:00:00", "tres"),
            error='Malformated limit!'
        )

    def test_top_with_values(self):
        self._test_top_success(
            values=('["KBS", "International Radio"]',  "2020-01-03T00:00:00", 10),
            length=3
        )

    def test_top_with_limit(self):
        self._test_top_success(
            values=('["KBS", "International Radio"]',  "2020-01-03T00:00:00", 2),
            length=2
        )

    def test_top_with_no_values(self):
        self._test_top_success(
            values=('["KBS"]',  "2020-01-10T00:00:00", 10),
            length=0
        )
