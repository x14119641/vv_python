import zipfile


with zipfile.ZipFile(
    '/root/Desktop/violent_python/vv_python/chapter1/CH1/evil.zip',
    'r') as zf:
    zf.extractall()
