import tkinter as tk
from tkinter import simpledialog,filedialog, messagebox
from music_player import MusicPlayer
from db_connection import connect_to_db

class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.player = MusicPlayer()

        # GUI Elements
        self.song_listbox = tk.Listbox(self.root, width=50, height=15)
        self.song_listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Song", bg="lightblue", fg="black", command=self.add_song_to_database)
        self.add_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.load_button = tk.Button(self.root, text="Load Songs", bg="orange", fg="black", command=self.load_songs_from_database)
        self.load_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

        self.play_button = tk.Button(self.root, text="Play", bg="lightgreen", fg="black", command=self.play_song)
        self.play_button.grid(row=2, column=0, padx=10, pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", bg="red", fg="black", command=self.player.stop_song)
        self.stop_button.grid(row=2, column=1, padx=10, pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", bg="darkgreen", fg="white", command=self.player.pause_song)
        self.pause_button.grid(row=2, column=2, padx=10, pady=5)

        self.resume_button = tk.Button(self.root, text="Resume", bg="darkred", fg="white", command=self.player.resume_song)
        self.resume_button.grid(row=2, column=3, padx=10, pady=5)

        self.next_button = tk.Button(self.root, text="Next", bg="lightyellow", fg="black", command=self.player.play_next_song)
        self.next_button.grid(row=3, column=0, padx=10, pady=5)

        self.prev_button = tk.Button(self.root, text="Previous", bg="lightpink", fg="black", command=self.player.play_previous_song)
        self.prev_button.grid(row=3, column=1, padx=10, pady=5)

        self.shuffle_button = tk.Button(self.root, text="Shuffle", bg="purple", fg="white", command=self.player.shuffle_songs)
        self.shuffle_button.grid(row=3, column=2, padx=10, pady=5)

        self.like_button = tk.Button(self.root, text="Like", bg="cyan", fg="black", command=self.like_song)
        self.like_button.grid(row=3, column=3, padx=10, pady=5)

        self.liked_songs_button = tk.Button(self.root, text="View Liked Songs", bg="blue", fg="white", command=self.view_liked_songs)
        self.liked_songs_button.grid(row=4, column=0, columnspan=4, pady=5)


    def add_song_to_database(self):

        # Admin login
        admin_name = simpledialog.askstring("Admin Login", "Enter admin name")
        admin_password = simpledialog.askstring("Admin Login", "Enter admin password", show='*')

        # Check admin credentials
        if admin_name != "Nikhar" or admin_password != "Nik123":
            messagebox.showerror("Error", "Invalid admin credentials!")
            return

        # Use simpledialog.askstring to get text input from the user

        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        file_name = file_path.split("/")[-1]
        title = file_name.split("by")[0].strip()
        artist = (file_name.split("by")[-1].strip()).split(".")[0].strip()

        if not title or not artist or not file_path:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            query = "INSERT INTO songs (title, artist, file_path) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (title, artist, file_path))
            self.connection.commit()
            messagebox.showinfo("Success", "Song added to database!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add song: {e}")

    def load_songs_from_database(self):
        try:
            self.cursor.execute("SELECT * FROM songs")
            songs = self.cursor.fetchall()
            if not songs:
                messagebox.showinfo("Info", "No songs in the database!")
                return

            self.player.load_songs(songs)
            self.song_listbox.delete(0, tk.END)
            for song in songs:
                self.song_listbox.insert(tk.END, f"{song[0]}. {song[1]} by {song[2]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load songs: {e}")

    def play_song(self):
        if not self.player.song_list:
            messagebox.showinfo("Info", "No songs loaded. Please load songs first.")
            return

        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a song to play!")
            return

        index = selected[0]
        self.player.play_song_by_index(index)

    def like_song(self):
        if not self.player.song_list:
            messagebox.showinfo("Info", "No songs loaded. Please load songs first.")
            return

        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a song to like!")
            return

        song_id = self.player.song_list[selected[0]][0]
        try:
            query = "INSERT INTO liked_songs (song_id) VALUES (%s)"
            self.cursor.execute(query, (song_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Song liked successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to like song: {e}")

    def view_liked_songs(self):
        
        LikedSongsWindow(self.root, self.player, self.cursor, self.connection)

    def on_close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.player.stop_song()
        self.root.destroy()



class LikedSongsWindow:
    def __init__(self, parent, player, cursor, connection):
        self.parent = parent
        self.player = player
        self.cursor = cursor
        self.connection = connection
        self.liked_songs = []
        self.current_index = 0
        
        self.window = tk.Toplevel(parent)
        self.window.title("Liked Songs")
        
        self.song_listbox = tk.Listbox(self.window, width=50, height=15)
        self.song_listbox.grid(row=0, column=0, columnspan=4,  padx=10, pady=10)
        
        self.play_button = tk.Button(self.window, text="Play",  bg="lightgreen", fg="black", command=self.play_song)
        self.play_button.grid(row=1, column=0, columnspan=2,  padx=5, pady=5)
        
        self.stop_button = tk.Button(self.window, text="Stop",  bg="red", fg="black",  command=self.player.stop_song)
        self.stop_button.grid(row=1, column=2,  columnspan=2, padx=5, pady=5)
        
        self.remove_button = tk.Button(self.window, text="Remove from Liked",  bg="darkblue", fg="white",  command=self.remove_song)
        self.remove_button.grid(row=2, column=0, columnspan=4, pady=5)
        
        self.load_liked_songs()
    
    def load_liked_songs(self):
        try:
            self.cursor.execute("""
                SELECT songs.id, songs.title, songs.artist, songs.file_path 
                FROM liked_songs
                INNER JOIN songs ON liked_songs.song_id = songs.id
            """)
            self.liked_songs = self.cursor.fetchall()
            
            self.song_listbox.delete(0, tk.END)
            for song in self.liked_songs:
                self.song_listbox.insert(tk.END, f"{song[0]}. {song[1]} by {song[2]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load liked songs: {e}")
    
    def play_song(self):
        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a song to play!")
            return
        
        self.current_index = selected[0]
        self.index = self.liked_songs[self.current_index][0]
        self.player.play_song_by_id(self.index)
    
    def remove_song(self):
        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a song to remove!")
            return
        
        song_id = self.liked_songs[selected[0]][0]
        try:
            self.cursor.execute("DELETE FROM liked_songs WHERE song_id = %s", (song_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Song removed from liked songs!")
            self.load_liked_songs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove song: {e}")



# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
