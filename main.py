from music_player import MusicPlayer
from db_connection import connect_to_db

def main():
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()

    player = MusicPlayer()

    while True:
        print("\n--- Music Player Menu ---")
        print("1. Add Song to Database")
        print("2. Load Songs from Database")
        print("3. Play Song")
        print("4. Play Next Song")
        print("5. Play Previous Song")
        print("6. Shuffle Songs")
        print("7. Like a Song")
        print("8. View Liked Songs")
        print("9. Stop Song")
        print("10. Pause Song")
        print("11. Resume Song")
        print("12. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter song title: ")
            artist = input("Enter artist name: ")
            file_path = input("Enter file path: ")

            try:
                query = "INSERT INTO songs (title, artist, file_path) VALUES (%s, %s, %s)"
                cursor.execute(query, (title, artist, file_path))
                connection.commit()
                print("Song added successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            cursor.execute("SELECT * FROM songs")
            songs = cursor.fetchall()
            if songs:
                player.load_songs(songs)
                print("Songs loaded successfully!")
            else:
                print("No songs in the database!")

        elif choice == "3":
            if not player.song_list:
                print("No songs loaded. Please load songs first.")
                continue

            print("\n--- Songs in Database ---")
            for song in player.song_list:
                print(f"{song[0]}. {song[1]} by {song[2]}")

            song_id = input("Enter the song ID to play: ")
            song_indices = [song[0] for song in player.song_list]
            if int(song_id) in song_indices:
                index = song_indices.index(int(song_id))
                player.play_song_by_index(index)
            else:
                print("Invalid song ID!")

        elif choice == "4":
            player.play_next_song()

        elif choice == "5":
            player.play_previous_song()

        elif choice == "6":
            player.shuffle_songs()

        elif choice == "7":
            if not player.song_list:
                print("No songs loaded. Please load songs first.")
                continue

            print("\n--- Songs in Database ---")
            for song in player.song_list:
                print(f"{song[0]}. {song[1]} by {song[2]}")

            song_id = input("Enter the song ID to like: ")
            try:
                query = "INSERT INTO liked_songs (song_id) VALUES (%s)"
                cursor.execute(query, (song_id,))
                connection.commit()
                print("Song liked successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "8":
            cursor.execute("""
                SELECT songs.id, songs.title, songs.artist
                FROM liked_songs
                INNER JOIN songs ON liked_songs.song_id = songs.id
            """)
            liked_songs = cursor.fetchall()
            if liked_songs:
                print("\n--- Liked Songs ---")
                for song in liked_songs:
                    print(f"{song[0]}. {song[1]} by {song[2]}")
            else:
                print("No liked songs yet!")

        elif choice == "9":
            player.stop_song()

        elif choice == "10":
            player.pause_song()

        elif choice == "11":
            player.resume_song()

        elif choice == "12":
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
