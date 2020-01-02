import crypt

def test_pass(crypt_pass):
    salt = crypt_pass[0:2]
    with open('CH1/passwords.txt', 'r') as f:
        for word in f.readlines():
            print(word)
            word = word.strip('\n')
