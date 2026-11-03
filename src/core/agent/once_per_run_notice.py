class OncePerRunNotice:
    def __init__(self, text):
        self.text = text
        self.has_appeared = False

    def add_to(self, response):
        if self.has_appeared:
            return response

        self.has_appeared = True
        return f"{self.text}\n\n{response}"
