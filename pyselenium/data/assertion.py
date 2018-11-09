
def httpcodeAssersion(repsonse, codes=[200]):
    code = repsonse.status_code
    if isinstance(codes, str) or isinstance(codes, int):
        code = [code]
    if code not in codes:
        raise AssertionError('{} 不在响应列表中'.format(code))
