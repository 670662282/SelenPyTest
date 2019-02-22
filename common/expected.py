class response_code_contains:
    """An expectation for checking the code of a response.
    codes is the contains code
    returns True if the response code matches, false otherwise.
    """
    def __init__(self, codes=[200]):
        if isinstance(codes, (str, int)):
            codes = [codes]
        self.codes = codes

    def __call__(self, response):
        return True if response.code in self.codes else False

