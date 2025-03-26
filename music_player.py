import pygame
import os
import random

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_song_index = -1
        self.song_list = []

    def load_songs(self, songs):
        # Load the song list from the database.

        self.song_list = songs
        print("Songs loaded into the player.")

    def play_song_by_index(self, index):
        # Play a song by its index in the song list.

        if index < 0 or index >= len(self.song_list):
            print("Invalid song index!")
            return

        file_path = self.song_list[index][3]  # File path is the 4th element in the tuple
        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.current_song_index = index
            print(f"Playing: {self.song_list[index][1]} by {self.song_list[index][2]}")
        else:
            print("File not found!")

    def play_song_by_id(self, song_id):
        # Play a song by its ID.
        # Args:
            # song_id (int): The ID of the song to play.

        for index, song in enumerate(self.song_list):
            if song[0] == song_id:  # Assuming the ID is the first element in the tuple
                self.play_song_by_index(index)
                return
        print("Song not found!")

    def play_next_song(self):
        # Play the next song in the song list.

        if self.current_song_index + 1 < len(self.song_list):
            self.play_song_by_index(self.current_song_index + 1)
        else:
            print("This is the last song in the list.")

    def play_previous_song(self):
        # Play the previous song in the song list.

        if self.current_song_index > 0:
            self.play_song_by_index(self.current_song_index - 1)
        else:
            print("This is the first song in the list.")

    def shuffle_songs(self):
        # Shuffle the current song list.

        random.shuffle(self.song_list)
        self.current_song_index = -1
        print("Songs shuffled!")

    def stop_song(self):
        pygame.mixer.music.stop()
        print("Music stopped.")

    def pause_song(self):
        pygame.mixer.music.pause()
        print("Music paused.")

    def resume_song(self):
        pygame.mixer.music.unpause()
        print("Music resumed.")
