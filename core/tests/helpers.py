# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import resolve


def test_resolution_template(testcase, url, url_name, template_file,
                             response_code=200):
    """
    Validates the url resolution and template used for a view.

    Performs the following checks:

    * url resolves to url_name
    * GET on url used the provided template file
    * GET on url returns the provided status code

    :param testcase: The Django TestCase to use for assertions.
    :param url: The raw url to use.
    :param url_name: The name that url should resolve to.
    :param template_file: The template file that should be used to render the
                          response on a GET request.
    :param response_code: The response code that should be returned on a GET
                          request.
    :returns: The response from a GET request.
    """
    match = resolve(url)
    testcase.assertEqual(match.url_name, url_name)
    response = testcase.client.get(url)
    testcase.assertTemplateUsed(response, template_file)
    testcase.assertEqual(response.status_code, response_code)
    return response
