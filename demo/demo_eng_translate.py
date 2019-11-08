import requests


def word_translate(word):
    data = {
    'doctype': 'json',
    'type': 'AUTO',
    'i':word
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    print(result)
    translate_result = result['translateResult'][0][0]["tgt"]
    # smartResult = result['smartResult']
    print(translate_result,type(translate_result))
    # print(smartResult)
    return translate_result

word_translate('word')
