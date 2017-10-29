# -*- coding: utf-8 -*-
import os

# 注意,这个常量必须保持文件夹中设置的分片大小一致
PIECE_SIZE = 5242880


class ReadableFolder(object):
    """将文件夹封装为file-like object。
    
    """
    def __init__(self, folder_name, total, length, full_path):
        self._folder_name = folder_name
        self._length = length
        self._size = self._remaining = PIECE_SIZE
        self._total = total
        self._full_path = full_path
        self._index = 0
        self._position = 0
        self._readable = None

    @property
    def file_name(self):
        return os.path.join(self._full_path, self._folder_name + '_' + str(self._index))

    def get_last_size(self):
        y = self._length % PIECE_SIZE
        return y if y else PIECE_SIZE

    def read(self, size=-1):
        if self._index >= self._total:
            return ''

        to_read = self._remaining if size < 0 else min(size, self._remaining)
        if not self._readable:
            self._readable = open(self.file_name, 'rb')
        self._readable.seek(self._position)
        chunk = self._readable.read(to_read)
        self._position = self._readable.tell()
        self._remaining -= len(chunk)
        if self._remaining <= 0:
            self._readable.close()
            self._readable = None
            self._index += 1
            if self._index == self._total - 1:
                self._size = self.get_last_size()
            self._remaining = self._size
            self._position = 0
        return chunk

    def reset(self):
        self._index = 0
        self._size = self._remaining = PIECE_SIZE
        self._position = 0
        if self._readable:
            self._readable.close()
            self._readable = None




