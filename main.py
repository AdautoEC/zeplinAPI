import requests
import json
import matplotlib
from munch import DefaultMunch
import xml.etree.ElementTree as et

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


def rgba_to_hex(rgba):
    return '%02x%02x%02x%02X' % rgba


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


def get_save_json(tag):
    write_file(
        tag,
        send_get_request_project(tag).json()
    )


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


def add_tag_xml(tag, value, attrs):
    new_color = et.SubElement(my_root, tag)
    new_color.text = value
    for attr in attrs:
        new_color.set(attr[0], attr[1])


def color_obj2xml(colors):
    for color in colors:
        attributes = [('name', color.name.replace(' ', '_').replace('-', '_').lower()), ('id', color.id)]
        add_tag_xml('color', '#' + rgba_to_hex((color.r, color.g, color.b, color.a * 255)), attributes)


def formatter_xml_file():
    file = open(xml_file_name, 'r')
    new_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + file.read()
    file.close()
    file = open(xml_file_name, 'w')
    file.write(new_xml)
    file.close()


if __name__ == '__main__':
    xml_file_name = 'res/values/colors.xml'
    id_project = get_id_first_project()
    my_tree = et.parse(xml_file_name)
    my_root = my_tree.getroot()
    color_obj2xml(json2class(get_colors()))
    my_tree.write(xml_file_name)
    formatter_xml_file()
    '''get_save_json('colors')
    get_save_json('text_styles')
    get_save_json('components')
    get_save_json('design_tokens')
    get_save_json('screens')'''
