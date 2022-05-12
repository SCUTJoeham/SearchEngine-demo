from django.shortcuts import render
from django.shortcuts import HttpResponse
from search.models import InvertedIndex
from search.models import News
import json
# Create your views here.


def get_news(urls):
    if len(urls) > 20:
        urls = urls[:20]
    res = []
    count = 0
    for url in urls:
        count = count + 1
        title = '' + News.objects.get(url=url).title
        content = '' + News.objects.get(url=url).content
        if len(content) > 400:
            content = content[:400]
        res.append({'id':count, 'url': url, 'title': title, 'content': content})
    return res


def search(request):
    result = dict()
    query = '' + request.GET.get("query")
    tokens = query.strip().split(' ')
    dict_li = []
    for token in tokens:
        url_dict = dict()
        ret = InvertedIndex.objects.filter(term=token.lower())
        if ret:
            ul_string = '' + ret[0].urllist
        else:
            continue
        url_nums = ul_string.split(';')
        for url_num in url_nums:
            if len(url_num):
                url, num = url_num.split('#')
                url_dict.update({url: int(num)})
        if url_dict:
            dict_li.append(url_dict)

    if len(dict_li) == 1:
        url_di = dict_li[0]
        urls = [k for k, v in sorted(url_di.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)]
        res = get_news(urls)
        result.update({'search_result': res})
    else:
        size = len(dict_li)
        urls = set()
        for shift in range(1, size):
            for i in range(size):
                if i + shift < size:
                    inters = set(dict_li[i].keys()).intersection(set(dict_li[i + shift].keys()))
                    inters = sorted(list(inters), key=lambda it: (dict_li[i].get(it) + dict_li[i + shift].get(it)),
                                    reverse=True)
                    urls.update(set(inters))
        res = get_news(list(urls))
        result.update({'search_result': res})

    if not result:
        res = "No result found"
        result.update({'search_result': res})

    result['key_word'] = query
    result['search_title'] = 'one'
    # print(result)

    return HttpResponse(json.dumps(result))
