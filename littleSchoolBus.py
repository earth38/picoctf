# 出力をlessで受け取り、"flag"で検索
import struct

f = open("littleschoolbus.bmp", "rb")

# ヘッダ部分はとばす
byte = f.read(54)
s = ""

# バイトごとにLSBの値を取得していき、8bitたまったら文字として表示する
while byte!="":
    try:
        byte=struct.unpack("B",f.read(1))[0]
    except:
        print("reading is over")
        exit()
    # LSBだけ取得
    byte = byte & 0b0000001
    s = s + str(byte)    

    # 8bit取得した場合
    if len(s) == 8:
        print(chr(int(s,2)), end="")
        s = ""
