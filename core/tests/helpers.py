# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import resolve, reverse


def test_resolution_template(testcase, url, url_name, template_file,
                             response_code=200, valid_lookup=None,
                             invalid_lookup=None):
    """
    Validates the url resolution and template used for a view.

    Performs the following checks:

    * url resolves to url_name
    * GET on url used the provided template file
    * GET on url returns the provided status code

    Optionally performs additional checks if provided information:

    * provided valid lookup url argument returns the provided status code
    * provided invalid lookup url argument returns 404

    :param testcase: The Django TestCase to use for assertions.
    :param url: The raw url to use.
    :param url_name: The name that url should resolve to.
    :param template_file: The template file that should be used to render the
                          response on a GET request.
    :param response_code: The response code that should be returned on a GET
                          request.
    :param valid_lookup: The arg to pass to the url that should resolve
                         successfully.
    :param invalid_lookup: The arg to pass to the url that should not resolve
                           successfully, resulting in a 404.
    :returns: The response from a GET request.
    """
    match = resolve(url)
    testcase.assertEqual(match.url_name, url_name)
    response = testcase.client.get(url)
    testcase.assertTemplateUsed(response, template_file)
    testcase.assertEqual(response.status_code, response_code)

    if valid_lookup is not None:
        valid_url = reverse(url_name, args=(valid_lookup,))
        valid_response = testcase.client.get(valid_url)
        testcase.assertEqual(valid_response.status_code, response_code)

    if invalid_lookup is not None:
        invalid_url = reverse(url_name, args=(invalid_lookup,))
        invalid_response = testcase.client.get(invalid_url)
        testcase.assertEqual(invalid_response.status_code, 404)

    return response
