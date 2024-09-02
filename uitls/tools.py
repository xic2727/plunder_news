import hashlib

def calculate_md5(text):
    # 创建一个md5对象
    md5_obj = hashlib.md5()
    # 更新md5对象
    md5_obj.update(text.encode("utf-8"))
    # 获取十六进制的MD5值
    md5_hex = md5_obj.hexdigest()
    return md5_hex