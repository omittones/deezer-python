import pytest
import deezer
from .base import BaseTestCaseWithVcr


class TestClient(BaseTestCaseWithVcr):
    def test_access_token_set(self):
        """Test that access token is set on the client."""
        self.client.access_token = "token"
        self.assertEqual(self.client.access_token, "token")
        self.assertEqual(
            self.client.object_url("user", "me"),
            "https://api.deezer.com/user/me?access_token=token",
        )

    def test_kwargs_parsing_valid(self):
        """Test that valid kwargs are stored as properties on the client."""
        self.assertEqual(self.client.app_id, "foo")
        self.assertEqual(self.client.app_secret, "bar")

    def test_ssl(self):
        """Test that the ssl parameter provides the right scheme"""
        self.assertEqual(self.client.scheme, "https")
        self.assertEqual(self.unsec_client.scheme, "http")

    def test_url(self):
        """Test the url() method
        it should add / to the request if not present
        """
        self.client.url()
        user = self.client.url("/user")
        self.assertEqual(user, "https://api.deezer.com/user")
        user = self.client.url("user")
        self.assertEqual(user, "https://api.deezer.com/user")

    def test_object_url(self):
        """Test the object_url() method, validates against the allowed types
        of objects"""
        self.assertEqual(
            self.client.object_url("album"), "https://api.deezer.com/album"
        )
        self.assertEqual(
            self.client.object_url("album", 12), "https://api.deezer.com/album/12"
        )
        self.assertEqual(
            self.client.object_url("album", "12"), "https://api.deezer.com/album/12"
        )
        self.assertEqual(
            self.client.object_url("album", "12", "artist"),
            "https://api.deezer.com/album/12/artist",
        )
        self.assertEqual(
            self.client.object_url("album", "12", limit=1),
            "https://api.deezer.com/album/12?limit=1",
        )
        self.assertEqual(
            self.client.object_url("album", "12", "artist", limit=1),
            "https://api.deezer.com/album/12/artist?limit=1",
        )
        self.assertEqual(
            self.client.object_url("artist", "12", "albums", limit=1),
            "https://api.deezer.com/artist/12/albums?limit=1",
        )
        self.assertRaises(TypeError, self.client.object_url, "foo")

    def test_get_album(self):
        """Test method to retrieve an album"""
        album = self.client.get_album(302127)
        self.assertIsInstance(album, deezer.resources.Album)

    def test_no_album_raise(self):
        """Test method get_album for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_album(-1)

    def test_get_artist(self):
        """Test methods to get an artist"""
        artist = self.client.get_artist(27)
        self.assertIsInstance(artist, deezer.resources.Artist)

    def test_no_artist_raise(self):
        """Test method get_artist for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_artist(-1)

    def test_get_comment(self):
        """Test methods to get a comment"""
        comment = self.client.get_comment(2772704)
        self.assertIsInstance(comment, deezer.resources.Comment)

    def test_no_comment_raise(self):
        """Test method get_comment for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_comment(-1)

    def test_get_genre(self):
        """Test methods to get a genre"""
        genre = self.client.get_genre(106)
        self.assertIsInstance(genre, deezer.resources.Genre)

    def test_no_genre_raise(self):
        """Test method get_genre for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_genre(-1)

    def test_get_genres(self):
        """Test methods to get several genres"""
        genres = self.client.get_genres()
        self.assertIsInstance(genres, list)
        self.assertIsInstance(genres[0], deezer.resources.Genre)

    def test_get_playlist(self):
        """Test methods to get a playlist"""
        playlist = self.client.get_playlist(908622995)
        self.assertIsInstance(playlist, deezer.resources.Playlist)

    def test_no_playlist_raise(self):
        """Test method get_playlist for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_playlist(-1)

    def test_get_radio(self):
        """Test methods to get a radio"""
        radio = self.client.get_radio(23261)
        self.assertIsInstance(radio, deezer.resources.Radio)

    def test_no_radio_raise(self):
        """Test method get_radio for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_radio(-1)

    def test_get_radios(self):
        """Test methods to get a radios"""
        radios = self.client.get_radios()
        self.assertIsInstance(radios, list)
        self.assertIsInstance(radios[0], deezer.resources.Radio)

    def test_get_track(self):
        """Test methods to get a track"""
        track = self.client.get_track(3135556)
        self.assertIsInstance(track, deezer.resources.Track)

    def test_no_track_raise(self):
        """Test method get_track for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_track(-1)

    def test_get_user(self):
        """Test methods to get a user"""
        user = self.client.get_user(359622)
        self.assertIsInstance(user, deezer.resources.User)

    def test_no_user_raise(self):
        """Test method get_user for invalid value"""
        with pytest.raises(ValueError):
            self.client.get_user(-1)

    def test_chart(self):
        self.assertEqual(
            self.client.object_url("chart"), "https://api.deezer.com/chart"
        )
        result = self.client.get_chart()
        self.assertIsInstance(result, deezer.resources.Chart)

        self.assertIsInstance(result.tracks[0], deezer.resources.Track)
        self.assertIsInstance(result.albums[0], deezer.resources.Album)
        self.assertIsInstance(result.artists[0], deezer.resources.Artist)
        self.assertIsInstance(result.playlists[0], deezer.resources.Playlist)

    def test_chart_tracks(self):
        result = self.client.get_chart("tracks")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Khapta")
        self.assertIsInstance(result[0], deezer.resources.Track)

    def test_chart_albums(self):
        result = self.client.get_chart("albums")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Lacrim")
        self.assertIsInstance(result[0], deezer.resources.Album)

    def test_chart_artists(self):
        result = self.client.get_chart("artists")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].name, "Lacrim")
        self.assertIsInstance(result[0], deezer.resources.Artist)

    def test_chart_playlists(self):
        result = self.client.get_chart("playlists")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Les titres du moment")
        self.assertIsInstance(result[0], deezer.resources.Playlist)

    def test_options_1(self):
        """Test a query with extra arguments"""
        result = self.client.search("Billy Jean", limit=2)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 2)

    def test_options_2(self):
        """Test a query with extra arguments"""
        result = self.client.search("Billy Jean", limit=2, index=1)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 2)

    def test_search_simple(self):
        """Test search method"""
        self.assertEqual(
            self.client.object_url("search", q="Soliloquy"),
            "https://api.deezer.com/search?q=Soliloquy",
        )
        result = self.client.search("Soliloquy")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Too much")

    def test_search_with_relation(self):
        """Test search method with relation"""
        self.assertEqual(
            self.client.object_url("search", relation="album", q="Daft Punk"),
            "https://api.deezer.com/search/album?q=Daft+Punk",
        )
        result = self.client.search("Daft Punk", "album")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Random Access Memories")
        self.assertIsInstance(result[0], deezer.resources.Album)

        result = self.client.search("Daft Punk", "album", "0", "1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertNotEqual(
            result[0], self.client.search("Daft Punk", "album", "1", "1")
        )

    def test_advanced_search_simple(self):
        """Test advanced_search method: simple case with one term"""
        self.assertEqual(
            self.client.object_url("search", q='artist:"Lou Doillon"'),
            "https://api.deezer.com/search?q=artist%3A%22Lou+Doillon%22",
        )
        result = self.client.advanced_search({"artist": "Lou Doillon"})
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Too much")

    def test_advanced_search_complex(self):
        """Test advanced_search method: complex case with two term"""
        self.assertEqual(
            self.client.object_url("search", q='artist:"Lou Doillon" album:"Lay Low"'),
            (
                "https://api.deezer.com/search?"
                "q=artist%3A%22Lou+Doillon%22+album%3A%22Lay+Low%22"
            ),
        )
        result = self.client.advanced_search(
            {"artist": "Lou Doillon", "album": "Lay Low"}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Where To Start")

    def test_advanced_search_complex_with_relation(self):
        """Test advanced_search method: with relation"""
        # Two terms with a relation
        self.assertEqual(
            self.client.object_url(
                "search", relation="track", q='artist:"Lou Doillon" track:"Joke"'
            ),
            (
                "https://api.deezer.com/search/track?"
                "q=artist%3A%22Lou+Doillon%22+track%3A%22Joke%22"
            ),
        )
        result = self.client.advanced_search(
            {"artist": "Lou Doillon", "track": "Joke"}, relation="track"
        )
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "The joke")
        self.assertIsInstance(result[0], deezer.resources.Track)

    def test_with_language_header_fr(self):
        """Test by adding accept language headers"""
        genre = self.client_fr.get_genre(52)
        self.assertIsInstance(genre, deezer.resources.Genre)
        self.assertEqual(genre.name, "Chanson fran\u00e7aise")
        self.assertNotEqual(genre.name, "French Chanson")

    def test_with_language_header_ja(self):
        """Test by adding accept language headers"""
        genre = self.client_ja.get_genre(52)
        self.assertIsInstance(genre, deezer.resources.Genre)
        self.assertEqual(
            genre.name, "\u30d5\u30ec\u30f3\u30c1\u30fb\u30b7\u30e3\u30f3\u30bd\u30f3"
        )
        self.assertNotEqual(genre.name, "French Chanson")
