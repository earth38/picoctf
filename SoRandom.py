# python2で実行すること。python3ではエラーは起きないがflagは表示されｒない
#!/usr/bin/python -u
import random,string

# 「nc shell2017.picoctf.com:37968」で取得した暗号文
enc_flag = "BNZQ:jn0y1313td7975784y0361tp3xou1g44"
a = []
random.seed("random")

#seed("random")から算出される乱数を配列にいれておく
for c in enc_flag:
  if c.islower():
    a.append(random.randrange(0,26))
  elif c.isupper():
    a.append(random.randrange(0,26))
  elif c.isdigit():
    a.append(random.randrange(0,10))
  elif c==":":
    a.append(30)

s = "a"
flag = ""
result = ""
j = 0

# 乱数の初期化。randrange()は再度同じ順序で乱数を算出する
random.seed("random")

# [a-zA-Z0-9]に対して、一文字ずつ同じ暗号処理を行い、暗号文と一致したらflagに加えていく
# 暗号処理は[a-zA-Z0-9]以外には暗号処理は行われていない
for r in enc_flag:
    if a[j] == 30:
        flag = flag+":"
        j = j + 1
        continue

    for i in range(62):
        if s.islower():
            result = chr((ord(s)-ord('a')+a[j])%26 + ord('a'))
        elif s.isupper():
            result = chr((ord(s)-ord('A')+a[j])%26 + ord('A'))
        elif s.isdigit():
            result = chr((ord(s)-ord('0')+a[j])%10 + ord('0'))
        else:
            pass
 
        
        if result == r:
            flag = flag + s
            s = "a"
            break
        
        if s == "z":
            s = "A"
        elif s == "Z":
            s = "0"
        else:
            s = chr(ord(s)+1)
        
    j = j + 1    
 
# flagの表示
print(flag)
