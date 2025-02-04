import tkinter as tk
from tkinter import messagebox
from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()
prolog.consult('dataset.pl')

def query_prolog(query):
    result = list(prolog.query(query))
    print(result)
    return result

def search_movies():
    title = title_entry.get() or ''
    genre = genre_entry.get() or ''
    director = director_entry.get() or ''
    actor = actor_entry.get() or ''
    year = year_entry.get() or ''
    duration = duration_entry.get() or ''
    rating = rating_entry.get() or ''

    query = "peliculas_por_condiciones('{}', '{}', '{}', '{}', {}, {}, {}, Peliculas)".format(
        title, genre, director, actor,
        year if year != '' else "''",
        duration if duration != '' else "''",
        rating if rating != '' else "''"
    )
    try:
        result = query_prolog(query)
        print(query)
        result_text.delete(1.0, tk.END)
        if result != [{'Peliculas': []}]:
            for movie in result[0]['Peliculas']:
                movie_details = "Title: {}, Genre: {}, Director: {}, Actor: {}, Year: {}, Duration: {}, Rating: {}".format(
                    movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6]
                )
                result_text.insert(tk.END, movie_details + "\n")
        else:
            result_text.insert(tk.END, "No movies found.")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))

def add_to_favorites():
    title = favorite_entry.get()
    query = "add_to_favorites('{}')".format(title)
    try:
        result = query_prolog(query)
        if result:
            update_favorite_list()
        else:
            messagebox.showerror("Error", "Movie not found or already in favorites.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def remove_from_favorites():
    title = favorite_entry.get()
    query = "remove_from_favorites('{}')".format(title)
    try:
        result = query_prolog(query)
        if result:
            update_favorite_list()
        else:
            messagebox.showerror("Error", "Movie not found in favorites.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_favorite_list():
    query = "get_favorite_movies(FavoriteMovies)"
    try:
        result = query_prolog(query)
        favorite_text.delete(1.0, tk.END)
        for movie in result[0]['FavoriteMovies']:
            favorite_text.insert(tk.END, movie + "\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def recommend_movies():
    query = "recommend_movies_based_on_favorites(RecommendedMovies)"
    try:
        result = query_prolog(query)
        recommendation_text.delete(1.0, tk.END)
        if result:
            for movie in result[0]['RecommendedMovies']:
                movie_details = "Title: {}, Genre: {}, Director: {}, Actor: {}, Year: {}, Duration: {}, Rating: {}".format(
                    movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6]
                )
                recommendation_text.insert(tk.END, movie_details + "\n")
        else:
            recommendation_text.insert(tk.END, "No recommendations found.")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Movie Search and Favorites")

# Create and place the title label
tk.Label(root, text="Movie Recommendation System", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Create and place the input fields and labels for search
tk.Label(root, text="Title:").grid(row=1, column=0, padx=20)
title_entry = tk.Entry(root)
title_entry.grid(row=1, column=1, padx=20)

tk.Label(root, text="Genre:").grid(row=2, column=0, padx=20)
genre_entry = tk.Entry(root)
genre_entry.grid(row=2, column=1, padx=20)

tk.Label(root, text="Director:").grid(row=3, column=0, padx=20)
director_entry = tk.Entry(root)
director_entry.grid(row=3, column=1, padx=20)

tk.Label(root, text="Actor:").grid(row=4, column=0, padx=20)
actor_entry = tk.Entry(root)
actor_entry.grid(row=4, column=1, padx=20)

tk.Label(root, text="Year:").grid(row=5, column=0, padx=20)
year_entry = tk.Entry(root)
year_entry.grid(row=5, column=1, padx=20)

tk.Label(root, text="Duration:").grid(row=6, column=0, padx=20)
duration_entry = tk.Entry(root)
duration_entry.grid(row=6, column=1, padx=20)

tk.Label(root, text="Rating:").grid(row=7, column=0, padx=20)
rating_entry = tk.Entry(root)
rating_entry.grid(row=7, column=1, padx=20)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=search_movies)
search_button.grid(row=8, column=0, columnspan=2, padx=20)

# Create and place the text area for results
result_text = tk.Text(root, height=5, width=100)
result_text.grid(row=9, column=0, columnspan=2, padx=20)

# Create and place the input field and label for adding to favorites
tk.Label(root, text="Add/Remove from Favorites:").grid(row=10, column=0, padx=20)
favorite_entry = tk.Entry(root)
favorite_entry.grid(row=10, column=1, padx=20)

# Create and place the add to favorites button
add_button = tk.Button(root, text="Add", command=add_to_favorites)
add_button.grid(row=11, column=0, columnspan=2, padx=20)

# Create and place the remove from favorites button
remove_button = tk.Button(root, text="Remove", command=remove_from_favorites)
remove_button.grid(row=12, column=0, columnspan=2, padx=20)

# Create and place the text area for favorite movies
favorite_text = tk.Text(root, height=5, width=100)
favorite_text.grid(row=13, column=0, columnspan=2, padx=20)

# Create and place the recommend button
recommend_button = tk.Button(root, text="Recommend", command=recommend_movies)
recommend_button.grid(row=14, column=0, columnspan=2, padx=20)

# Create and place the text area for recommendations
recommendation_text = tk.Text(root, height=10, width=100)
recommendation_text.grid(row=15, column=0, columnspan=2, padx=20)

# Run the main loop
root.mainloop()