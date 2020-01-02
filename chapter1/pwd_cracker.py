import crypt

def test_pass(crypt_pass):
    salt = crypt_pass[0:2]
    with open(r'chapter1\CH1\dictionary.txt') as f:
        for word in f.readlines():
            print(word)
            word = word.strip('\n')


if __name__=='__main__':
    test_pass([])
