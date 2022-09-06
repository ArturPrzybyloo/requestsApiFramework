class ResponseStatusCodeNotMatchedException(Exception):
    pass


def verify_response_status_code(response, expected_status_code):
    if response.status_code != expected_status_code:
        raise ResponseStatusCodeNotMatchedException(f'Expected status code: {expected_status_code} but found: '
                                                    f'{response.status_code} \n with response: {response.text}')
