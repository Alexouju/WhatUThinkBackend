class Picture:
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"Picture(url='{self.url}')"