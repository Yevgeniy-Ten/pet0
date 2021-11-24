def generate_id():
    id = 1
    while True:
        yield id
        id += 1


id = generate_id()


class Movie:
    def __init__(self, name, img_url, description="", rating=0):
        self.id = next(id)
        self.name = name
        self.img_url = img_url
        self.description = description
        self.rating = rating

    def __str__(self):
        return f'{self.id} {self.name}'


class DBMovie:
    def __init__(self):
        self.movies = []

    def get(self):
        return self.movies

    def find_by_id(self, id):
        for movie in self.movies:
            if movie.id == id:
                return movie

    def delete_by_id(self, id):
        movie_for_delete = self.find_by_id(id)
        self.movies.remove(movie_for_delete)

    def save(self, movie):
        self.movies.append(movie)

    def filter_by_categories(self, category):
        pass
