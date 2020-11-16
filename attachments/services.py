from knowledge.models import KbKnowledge
import json
from urllib.parse import quote, unquote
import requests


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


def check_image_url(url):
    result = {
        "output": {
            "detections": [
                {
                    "confidence": "0.86",
                    "bounding_box": [
                        30,
                        518,
                        183,
                        190
                    ],
                    "name": "Female Breast - Exposed"
                },
                {
                    "confidence": "0.97",
                    "bounding_box": [
                        291,
                        541,
                        213,
                        209
                    ],
                    "name": "Female Breast - Exposed"
                },
                {
                    "confidence": "0.97",
                    "bounding_box": [
                        496,
                        736,
                        221,
                        241
                    ],
                    "name": "Female Breast - Exposed"
                },
                {
                    "confidence": "0.96",
                    "bounding_box": [
                        776,
                        740,
                        205,
                        221
                    ],
                    "name": "Female Breast - Exposed"
                }
            ],
            "nsfw_score": 0.996852695941925
        },
        "id": "4b24ae93-e453-4494-a915-c0cf733e38f1"
    }
    # image_url = url
    # r = requests.post(
    #     "https://api.deepai.org/api/nsfw-detector",
    #     data={
    #         'image': image_url,
    #     },
    #     headers={'api-key': 'd50664e4-cbb3-4d11-9a92-56de027f74b4'}
    # )
    # return r.json(), r.status_code
    return result, 200
