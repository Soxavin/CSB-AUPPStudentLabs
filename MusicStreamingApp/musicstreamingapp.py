"""
You are part of a team developing a new music streaming app called "MFun." Your task is to design the core functionality that manages the user's music library and playlist creation. Consider the following requirements:

Music library:
Needs to store a collection of songs and their associated metadata (title, artist, album, genre, length).
Must efficiently retrieve songs by various criteria (artist, album, genre, title).
Must prevent duplicate song entries.

Playlists:
Users can create unlimited playlists.
Each playlist can contain any number of songs, but a song cannot be added multiple times to the same playlist.
Songs can be added, removed, or reordered within playlists.
The app should display songs in the order they were added to the playlist.

Which data structure model(s) would you choose to implement the music library and playlist features? Explain your choices, considering the characteristics of each data structure and the specific requirements of the application.

Data structures to consider:
       Tuples, Sets, Lists, Dictionaries, Trees, Graphs, Stacks, Queues
"""



class Song:
    def __init__(self, title, artist, album, genre, length):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.length = length


class MusicLibrary:
    def __init__(self):
        self.songs = {}

    def add_song(self, song):
        if song.title not in self.songs:
            self.songs[song.title] = song

    def get_songs_by_artist(self, artist):
        return [song for song in self.songs.values() if song.artist == artist]

    def get_songs_by_album(self, album):
        return [song for song in self.songs.values() if song.album == album]

    def get_songs_by_genre(self, genre):
        return [song for song in self.songs.values() if song.genre == genre]

    def get_songs_by_title(self, title):
        return self.songs.get(title, None)


class Playlist:
    def __init__(self, name, music_library):
        self.name = name
        self.songs = []
        self.library = music_library

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)

    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            print("Song removed from the playlist.")

    def reorder_songs(self, new_order):
        new_songs = [self.library.get_songs_by_title(title) for title in new_order if self.library.get_songs_by_title(title)]

        # Check if the new order contains all the songs in the playlist
        if len(new_songs) == len(self.songs) and all(new_songs):
            self.songs = new_songs
            print("Playlist reordered.")
        else:
            print("Invalid new order. Please ensure all song titles are correct and exist in the library. The playlist remains unchanged.")



    def display_playlist(self):
        print(f"\nPlaylist: {self.name}")
        for i, song in enumerate(self.songs, start=1):
            print(f"{i}. {song.title} - {song.artist}")


def main():
    library = MusicLibrary()
    playlists = []

    while True:
        print("\nOptions:")
        print("1. Add Song to Library")
        print("2. Create Playlist")
        print("3. Add Song to Playlist")
        print("4. Display Playlists")
        print("5. Remove Song from Playlist")
        print("6. Reorder Songs in Playlist")
        print("7. Search Songs by Artist")
        print("8. Exit")

        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            title = input("Enter song title: ")
            artist = input("Enter artist: ")
            album = input("Enter album: ")
            genre = input("Enter genre: ")

            # Error handling for invalid input when converting to float
            try:
                length = float(input("Enter length (in minutes): "))
            except ValueError:
                print("Invalid input for length. Please enter a valid number.")
                continue

            song = Song(title, artist, album, genre, length)
            library.add_song(song)
            print("Song added to the library.")

        elif choice == 2:
            name = input("Enter playlist name: ")
            playlist = Playlist(name, library)
            playlists.append(playlist)
            print("Playlist created.")

        elif choice == 3:
            playlist_name = input("Enter playlist name: ")
            playlist = next((p for p in playlists if p.name == playlist_name), None)
            if playlist:
                title = input("Enter song title to add: ")
                song = library.get_songs_by_title(title)
                if song:
                    playlist.add_song(song)
                    print("Song added to the playlist.")
                else:
                    print("Song not found in the library.")
            else:
                print("Playlist not found.")

        elif choice == 4:
            if not playlists:
                print("You currently have no playlists. Please create some new playlists.")
            else:
                for playlist in playlists:
                    playlist.display_playlist()

        elif choice == 5:
            playlist_name = input("Enter playlist name: ")
            playlist = next((p for p in playlists if p.name == playlist_name), None)
            if playlist:
                title = input("Enter song title to remove: ")
                song = library.get_songs_by_title(title)
                if song in playlist.songs:
                    playlist.remove_song(song)
                else:
                    print("Song not found in the playlist.")
            else:
                print("Playlist not found.")

        elif choice == 6:
            playlist_name = input("Enter playlist name: ")
            playlist = next((p for p in playlists if p.name == playlist_name), None)
            if playlist:
                new_order = input("Enter the new order of song titles (comma-separated): ").split(',')
                playlist.reorder_songs(new_order)
            else:
                print("Playlist not found.")

        elif choice == 7:
            artist_name = input("Enter artist name to search: ")
            songs_by_artist = library.get_songs_by_artist(artist_name)
            if songs_by_artist:
                print(f"\nSongs by {artist_name}:")
                for song in songs_by_artist:
                    print(f"{song.title} - {song.album}")
            else:
                print(f"No songs found by {artist_name}.")

        elif choice == 8:
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
