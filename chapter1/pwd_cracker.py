import crypt

def test_pass(crypt_pass):
    print(crypt_pass)
    salt = crypt_pass[0:2]
    print(salt)
    with open('/root/Desktop/violent_python/vv_python/chapter1/CH1/dictionary.txt', 'r') as f:
        words = f.read().split('\n')
    for word in words[:-1]:
        crypt_word = crypt.crypt(word, salt)
        if crypt_word == crypt_pass:
            print(f'Found password: {word}')
            return
    print('Not password found')
    return

def main():
    with open('/root/Desktop/violent_python/vv_python/chapter1/CH1/passwords.txt', 'r') as f:
        for line in f.readlines():
            if ':' in line:
                user = line.split(':')[0]
                print(user)
                crypt_pass = line.split(':')[1].strip(' ')
                test_pass(crypt_pass)

if __name__ == '__main__':
    main()
