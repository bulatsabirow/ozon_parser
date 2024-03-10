from urllib.parse import urlencode


class BasePaginationMixin:
    start_url: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = 1
        self.start_urls = [*self.start_urls, self.get_paginated_page()]

    def get_query_params(self):
        return {"page": self.page}

    def get_paginated_page(self):
        return f'{self.start_url}?{urlencode(self.get_query_params())}'
