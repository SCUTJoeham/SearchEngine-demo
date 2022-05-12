import json
import pymysql

def clean_sentence(text):
    with open('stopwords.txt', 'r', encoding='UTF-8') as f:
        stop_word_list = f.readlines()
    text = text.lower()
    text_split = list(text)
    for i in range(len(text_split)):
        if text_split[i] < 'a' or text_split[i] > 'z':
            text_split[i] = ' '
    text = ''.join(text_split)

    text_list = text.split(' ')
    text_list = [x for x in text_list if x != '']
    for stop_word in stop_word_list:
        if stop_word.strip() in text_list:
            while text_list.count(stop_word.strip()) > 0:
                for word in text_list:
                    if word == stop_word.strip():
                        text_list.remove(stop_word.strip())
    return " ".join(text_list)

def store_news_to_database():
    conn = pymysql.connect(
        host='xxx',
        port=3306,
        user='root',
        passwd='xxx.',
        db='lab_1',
        charset='utf8'
    )
    cur = conn.cursor()

    with open('data.txt', 'r') as f:
        lines = f.readlines()
    lines = set(lines)
    count = 1
    for line in lines:
        line_json = json.loads(line)
        line_json["title"] = line_json["title"].replace("'", " ")
        line_json["main_body"] = line_json["main_body"].replace("'", " ")
        tokens = clean_sentence(line_json["title"]) + " " + clean_sentence(line_json["main_body"])
        tokens = tokens.strip()
        if len(tokens) < 3:
            continue
        # sql_statement = "INSERT INTO news(url,title,content,tokens) VALUES ('%s','%s','%s','%s')" % (
        # line_json["url"], line_json["title"], line_json["main_body"], tokens)
        sql_statement = "INSERT INTO search_news(url,title,content) VALUES ('%s','%s','%s')" % (
        line_json["url"], line_json["title"], line_json["main_body"])
        cur.execute(sql_statement)
        count = count + 1
        print(count, "sucess!")
    conn.commit()
    cur.close()
    conn.close()

def store_tokens_to_database():
    conn = pymysql.connect(
        host='xxx',
        port=3306,
        user='root',
        passwd='xxx.',
        db='lab_1',
        charset='utf8'
    )
    cur = conn.cursor()
    with open("inverted_index.txt","r") as f:
        lines = f.readlines()

    count = 1
    for line in lines:
        line_split = line.strip().split("\t")
        if len(line_split) != 2:
            continue
        sql_statement = "INSERT INTO search_invertedindex(term,urllist) VALUES ('%s','%s')" % (line_split[0], line_split[1])
        cur.execute(sql_statement)
        count = count + 1
        print(count, "sucess!")
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    store_tokens_to_database()
    store_news_to_database()