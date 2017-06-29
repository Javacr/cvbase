import os
from collections import OrderedDict

import pytest
from cvbase import Cache, VideoReader


class TestCache(object):

    def test_init(self):
        with pytest.raises(ValueError):
            Cache(0)
        cache = Cache(100)
        assert cache.capacity == 100
        assert cache.size == 0

    def test_put(self):
        cache = Cache(3)
        for i in range(1, 4):
            cache.put('key{}'.format(i), i)
            assert cache.size == i
        assert cache._cache == OrderedDict(
            [('key1', 1), ('key2', 2), ('key3', 3)])
        cache.put('key4', 4)
        assert cache.size == 3
        assert cache._cache == OrderedDict(
            [('key2', 2), ('key3', 3), ('key4', 4)])
        cache.put('key2', 2)
        assert cache._cache == OrderedDict(
            [('key2', 2), ('key3', 3), ('key4', 4)])

    def test_get(self):
        cache = Cache(3)
        assert cache.get('key_none') is None
        assert cache.get('key_none', 0) == 0
        cache.put('key1', 1)
        assert cache.get('key1') == 1


class TestImage(object):

    @classmethod
    def setup_class(cls):
        cls.video_path = os.path.join(
            os.path.dirname(__file__), 'data/test.mp4')

    def test_load(self):
        v = VideoReader(self.video_path)
        assert v.width == 294
        assert v.height == 240
        assert v.fps == 25
        assert v.frame_cnt == 168

    def test_read(self):
        v = VideoReader(self.video_path)
        _, img = v.read()
        assert int(round(img.mean())) == 94
        _, img = v.get_frame(64)
        assert int(round(img.mean())) == 94
        _, img = v.get_frame(65)
        assert int(round(img.mean())) == 205

    def test_current_frame(self):
        v = VideoReader(self.video_path)
        assert v.current_frame() is None
        v.read()
        img = v.current_frame()
        assert int(round(img.mean())) == 94

    def test_position(self):
        v = VideoReader(self.video_path)
        assert v.position == 0
        for _ in range(10):
            v.read()
        assert v.position == 10
        v.get_frame(100)
        assert v.position == 100

    def test_iterator(self):
        cnt = 0
        for img in VideoReader(self.video_path):
            cnt += 1
            assert img.shape == (240, 294, 3)
        assert cnt == 168

    def test_cvt2frames(self):
        v = VideoReader(self.video_path)
        frame_dir = '.cvbase_test'
        v.cvt2frames(frame_dir)
        assert os.path.isdir(frame_dir)
        for i in range(168):
            filename = '{}/{:06d}.jpg'.format(frame_dir, i)
            assert os.path.isfile(filename)
            os.remove(filename)
        os.removedirs(frame_dir)

        v = VideoReader(self.video_path)
        v.cvt2frames(
            frame_dir, filename_digit=3, start=100, file_start=100, ext='JPEG')
        assert os.path.isdir(frame_dir)
        for i in range(100, 168):
            filename = '{}/{:03d}.JPEG'.format(frame_dir, i)
            assert os.path.isfile(filename)
            os.remove(filename)
        os.removedirs(frame_dir)