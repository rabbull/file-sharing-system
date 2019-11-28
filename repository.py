import os
import hashlib
import json
import fcntl


def calculate_checksum(path):
    fp = open(path, 'rb')
    hashfunc = hashlib.md5()
    hashfunc.update(fp.read())
    result = hashfunc.hexdigest()
    fp.close()
    return result


class Repository(object):
    class Entry(object):
        def __init__(self, path: str = None):
            if not path:
                return

            if not os.path.exists(path):
                raise FileNotFoundError()

            # type
            if os.path.isdir(path):
                self.__type = 'dir'
                raise NotImplementedError()
            elif os.path.isfile(path):
                self.__type = 'file'
            elif os.path.islink(path):
                self.__type = 'link'
                raise NotImplementedError()
            else:
                raise NotImplementedError()

            self.__realpath = os.path.realpath(path)
            self.__basename = os.path.basename(path)
            self.__size = os.path.getsize(path)
            self.__checksum = calculate_checksum(path)

        @property
        def path(self):
            return self.__realpath

        @property
        def basename(self):
            return self.__basename

        @property
        def size(self):
            return self.__size

        @property
        def checksum(self):
            return self.__checksum

        def __eq__(self, another):
            return str(self.__dict__) == str(another.__dict__)

        def __str__(self):
            return json.dumps(self.__dict__)

    def __init__(self, repository_path):
        self.__path = repository_path

    def __read(self):
        print(self.__path)
        fp = open(self.__path, 'r+')
        print(fp)
        fcntl.lockf(fp, fcntl.LOCK_EX)
        content = fp.read()
        fcntl.lockf(fp, fcntl.LOCK_UN)
        fp.close()

        entries = []
        lst = json.loads(content)
        for i in range(len(lst)):
            e = self.Entry()
            e.__dict__ = lst[i]
            entries.append(e)
        return entries

    def __write(self, entries):
        entries = [entry.__dict__ for entry in entries]
        content = json.dumps(entries)
        fp = open(self.__path, 'w')
        fcntl.lockf(fp, fcntl.LOCK_UN)
        fp.write(content)
        fcntl.lockf(fp, fcntl.LOCK_UN)
        fp.close()

    def as_list(self):
        return self.__read()

    def add_entry(self, new_path):
        entries = self.__read()
        new_entry = self.Entry(new_path)
        if new_entry in entries:
            return
        entries.append(new_entry)
        self.__write(entries)

    def find(self, filename):
        entries = self.as_list()
        for entry in entries:
            if entry.basename == filename:
                return entry
        return None


if __name__ == '__main__':
    repo = Repository('repository')
    print(repo.as_list())
    repo.add_entry('.gitignore')
    print([r.__dict__ for r in repo.as_list()])
