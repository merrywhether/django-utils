def convert_to_querystring(query_dict, clean=True):
    """
    Convert QueryDict into querystring. Useful when doing the GET-POST-REDIRECT pattern.
    Cleans --Select-- and blank values from the querystring by default.
    """
    query_dict_copy = query_dict.copy()

    for query in query_dict:
        if query == 'csrfmiddlewaretoken':
            del query_dict_copy[query]
        elif clean and query_dict_copy[query] == '--Select--':
            del query_dict_copy[query]
        elif clean and not query_dict_copy[query]:
            del query_dict_copy[query]

    querystring = query_dict_copy.urlencode(True)
    return querystring
