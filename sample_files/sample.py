import os

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        print(data, file=f)

def append_file(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        print(data, file=f)

def delete_file(path):
    os.remove(path)

def does_file_exist(path):
    return os.path.isfile(path)

def get_files_in_directory(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

if __name__ == '__main__':
    print('Sample Python file')
    print('Another line')
    print('Yet another line')
    print('This is line 5')
    print('This is line 6')
    print('More content')
    print('Additional lines')
    print('Keep adding lines')
    print('Line 10')
    print('Line 11')
    print('Line 12')