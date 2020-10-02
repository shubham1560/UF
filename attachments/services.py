def get_the_link(request):
    # breakpoint()
    url = request.META['QUERY_STRING'].split("=")[1]
