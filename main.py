from flask import *
import pandas as pd
import pickle
import requests



movies_dict= pickle.load(open("movie_dict.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters



app = Flask(__name__)

@app.route("/")
def movie():
    return render_template("movie.html",res=movies["title"].values)

@app.route("/action",methods=["POST"])
def action():
    movie=request.form["movie"]
    movies,posters=recommend(movie)
    return render_template("show.html",res1=movies,poster=posters)


if __name__ =="__main__":
    app.run(debug=True)