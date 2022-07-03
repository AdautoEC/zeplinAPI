import requests
import json
from munch import DefaultMunch

'''
Description: This test script aims to capture the values coming from the Zeplin API and use them in 
Daycoval's mobile projects. 
Link_to_developer: https://app.zeplin.io/profile/developer
Documentation: https://docs.zeplin.dev/docs/getting-started-with-zeplin-api
Client_id: 62c0b9fc31ced8193a0dfed3
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicGVyc29uYWxfYWNjZXNzX3Rva2VuIiwiY2xpZW50X2l
kIjoiNjJjMGM2OTJkYTA2OWMxOGZmYjc3YWU4Iiwic2NvcGUiOiJhZG1pbiIsImlhdCI6MTY1NjgwMDkxNCwiZXhwIjoxOTcyMz
cwMTc0LCJpc3MiOiJ6ZXBsaW46YXBpLnplcGxpbi5pbyIsInN1YiI6IjU5Zjc5ODI0M2I1NjcxNjBjMGQ2NmFmZiIsImp0aSI6I
jJlZmUyNzkzLWY4ZGMtNDU3Yy05YmNiLTEyNDVkZjdiNTIzYyJ9.f-GkAEupxpttFj8alu15FN-5eApRPs7uwHtZbQBfRwQ
'''

base_url = 'https://api.zeplin.dev/v1/projects/'
header = {
    "Accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                     ".eyJ0eXBlIjoicGVyc29uYWxfYWNjZXNzX3Rva2VuIi"
                     "wiY2xpZW50X2lkIjoiNjJjMGM2OTJkYTA2OWMxOGZmY"
                     "jc3YWU4Iiwic2NvcGUiOiJhZG1pbiIsImlhdCI6MTY1"
                     "NjgwMDkxNCwiZXhwIjoxOTcyMzcwMTc0LCJpc3MiOiJ"
                     "6ZXBsaW46YXBpLnplcGxpbi5pbyIsInN1YiI6IjU5Zj"
                     "c5ODI0M2I1NjcxNjBjMGQ2NmFmZiIsImp0aSI6IjJlZ"
                     "mUyNzkzLWY4ZGMtNDU3Yy05YmNiLTEyNDVkZjdiNTIz"
                     "YyJ9.f-GkAEupxpttFj8alu15FN-5eApRPs7uwHtZbQBfRwQ"
}
get_all_projects_params = {
    'limit': 30,
    'status': 'active',
    'offset': 0
}
id_project = ""
highlighter = '--------------------------------------------------'


def json2class(json_object):
    return DefaultMunch.fromDict(json_object)


def write_file(tag, json_object):
    file = open('responses/' + tag + '.json', 'w')
    if type(json_object) == list:
        file.write(
            '[' +
            (",\n".join(str(obj) for obj in json_object)).replace('\'', '\"') +
            ']'
        )
    elif type(json_object) == dict:
        file.write(json.dumps(json_object).replace('\'', '\"'))
    else:
        file.write(json_object.replace('\'', '\"'))
    file.close()


def send_get_request(url, params=None):
    return requests.get(
        url=url,
        params=params,
        headers=header
    )


def send_get_request_project(url, params=None):
    return send_get_request(
        url=base_url + id_project + '/' + url,
        params=params
    )


def get_all_projects():
    return send_get_request(
        url=base_url,
        params=get_all_projects_params
    ).json()


def get_id_first_project():
    return get_all_projects()[0]['id']


def get_colors():
    return send_get_request_project('colors').json()


def get_text_styles():
    return send_get_request_project('text_styles').json()


def get_components():
    return send_get_request_project('components').json()


def get_design_tokens():
    return send_get_request_project('design_tokens').json()


def get_screens():
    return send_get_request_project('design_tokens').json()


if __name__ == '__main__':
    id_project = get_id_first_project()

    write_file('color', get_colors())
    write_file('text_styles', get_text_styles())
    write_file('components', get_components())
    write_file('design_tokens', get_design_tokens())
    write_file('screens', get_screens())
