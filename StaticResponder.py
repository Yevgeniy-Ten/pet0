from glob import glob
import os


class StaticResponder:
    def __init__(self, request, response, static_dir):
        self.request = request
        self.response = response
        self.static_dir = static_dir
        self.file = None
        self._check_file()

    def _check_file(self):
        file_uri = self.request.uri.replace("..", "")
        path = "./" + self.static_dir + file_uri
        files = glob(path)

        if len(files) > 0 and os.path.isfile(files[0]):
            self.file = files[0]

    def prepare_response(self):
        if self.file:
            file = open(self.file, "rb")
            self.response.set_file_body(file)
