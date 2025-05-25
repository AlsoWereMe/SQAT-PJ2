import hashlib
import pickle
import os

def dump_object(path: str, data):
    # 自动创建目录
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    # 写入文件
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load_object(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_md5_of_object(obj):
    serialized_obj = pickle.dumps(obj)
    md5_hash = hashlib.md5()
    md5_hash.update(serialized_obj)
    return md5_hash.hexdigest()
