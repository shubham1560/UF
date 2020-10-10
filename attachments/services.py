from knowledge.models import KbKnowledge
import json
from urllib.parse import quote, unquote


def get_the_link(request):
    # breakpoint()
    url = request.META['QUERY_STRING'].split("=")[1]
    return url


def get_the_url_link_data(request, article):
    # print(request.META['QUERY_STRING'])
    final_blocks = []
    arr_url_section = request.META['QUERY_STRING'].split('%23')
    # breakpoint()
    if len(arr_url_section) == 2:
        # breakpoint()
        section = arr_url_section[1]
        # arr_url_section[0] = arr_url_section[0].replace("/", '%2F')
        # article_id = arr_url_section[0].split('%2F')[-1]
        # article = KbKnowledge.objects.get(id=article_id)
        # article = article
        string_of_blocks = article.article_body[1: -1]
        blocks_string = string_obj(string_of_blocks)
        for block in blocks_string:
            final_blocks.append(json.loads(block))
        counter = 0
        headers = 0
        from_heading = 0
        for blocks in final_blocks:
            if blocks['type'] == "header":
                headers += 1
                if headers == 2:
                    to_heading = counter
                    result = final_blocks[from_heading: to_heading]
                    return result
                if quote(blocks['data']['text'], safe='') == unquote(section):
                    headers = 1
                    # pass
                    from_heading = counter
                    # return result
                else:
                    headers = 0
            counter += 1
        return final_blocks[from_heading: len(final_blocks)]
    else:
        return []


def string_obj(string):
    arr = []
    change_list = []
    counter = 0
    for i in string:
        if i == "{":
            arr.append("{")
        if i == "}":
            arr.pop()
        if len(arr) == 0 and i == ',':
            change_list.append(counter)
        counter += 1
    ind = change_list
    temp = list(string)
    for i in ind:
        temp[i] = '@@'
    final = ''.join(temp)
    return final.split('@@')

