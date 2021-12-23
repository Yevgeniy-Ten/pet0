from models import Movie, DBMovie
from urllib.parse import parse_qs
from response import Response

db_movie = DBMovie()
db_movie.save(
    Movie("Movie1", "https://image.api.playstation.com/vulcan/img/rnd/202010/2621/H9v5o8vP6RKkQtR77LIGrGDE.png"))
db_movie.save(
    Movie("Movie2", "https://image.api.playstation.com/vulcan/img/rnd/202010/2621/H9v5o8vP6RKkQtR77LIGrGDE.png"))
db_movie.save(
    Movie("Movie3", "https://image.api.playstation.com/vulcan/img/rnd/202010/2621/H9v5o8vP6RKkQtR77LIGrGDE.png"))


def show_movies(request, response):
    movies = db_movie.get()
    html_movies = ""
    for movie in movies:
        html_movies += f'''
        <div class="col">
                <div class="card">
                    <img src="{movie.img_url}" class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">{movie.id} {movie.name}</h5>
                        <p class="card-text">{movie.description}</p>
                        <a href="/movies/find?id={movie.id}" class="btn btn-primary">Detail</a>
                    </div>
                </div>
        </div>
        '''
    with open("templates/index.html", "r") as file:
        html = file.read()
        result_html = html.replace("{{movies}}", html_movies)
        response.set_body(result_html)


def show_movie(request, response):
    id = int(request.uri[-1])
    movie = db_movie.find_by_id(id)
    html_movie = f'''
    <div class="card" >
          <img src="{movie.img_url}" class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">Name: {movie.name}</h5>
            <p class="card-text">Description: {movie.description}.</p>
            <p class="card-text">Rating: {movie.rating}.</p>
          </div>
</div>
    '''
    with open("templates/detail.html", "r") as file:
        html = file.read()
        result_html = html.replace("{{movie}}", html_movie)
        response.set_body(result_html)


def create_movie(request, response):
    decoded_body = request.body.decode()
    body = parse_qs(decoded_body)
    movie = Movie(body['name'][0], body['img_url'][0], body['description'][0])
    db_movie.save(movie)
    response.set_status(Response.HTTP_REDIRECT_STATUS)
    response.add_header('Location', "/")


def find_one_movie(request, response):
    id_split = request.query.split("=")
    if len(id_split) > 1:
        id = id_split[1]
        movie = db_movie.find_by_id(int(id))
        html_movie = f'''
            <div class="card" >
                  <img src="{movie.img_url}" class="card-img-top" alt="...">
                  <div class="card-body">
                    <h5 class="card-title">Name: {movie.name}</h5>
                    <p class="card-text">Description: {movie.description}.</p>
                    <p class="card-text">Rating: {movie.rating}.</p>
                  </div>
        </div>
            '''
        with open("templates/detail.html", "r") as file:
            html = file.read()
            result_html = html.replace("{{movie}}", html_movie)
            response.set_body(result_html)
    else:
        pass


routes = {
    "/": show_movies,
    "/create": create_movie,
    "/movies/find": find_one_movie
}
