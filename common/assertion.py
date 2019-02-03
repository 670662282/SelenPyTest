def http_code_assertion(response, codes=[200]):
    code = response.status_code
    if isinstance(codes, str) or isinstance(codes, int):
        code = [code]
    if code not in codes:
        raise AssertionError('{} 不在响应列表中'.format(code))
