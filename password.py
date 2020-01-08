import hashlib

if __name__ == '__main__':
    pw = input('请输入密码：')
    pw = '{}cms'.format(pw)
    md5 = hashlib.md5()
    md5.update(pw.encode('utf-8'))
    hash_pw = md5.hexdigest()
    with open('./password', 'w') as fh:
        fh.write(hash_pw)
