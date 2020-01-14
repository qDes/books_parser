import unittest

from parser import download_txt


class TestDownload(unittest.TestCase):

    def test_path1(self):
        url = 'http://tululu.org/txt.php?id=1'
        filepath = download_txt(url, 'Алиби')
        self.assertEqual(filepath, 'books/Алиби.txt')

    def test_path2(self):
        url = 'http://tululu.org/txt.php?id=1'
        filepath = download_txt(url, 'Али/би', folder='books/')
        self.assertEqual(filepath, 'books/Алиби.txt')

    def test_path3(self):
        url = 'http://tululu.org/txt.php?id=1'
        filepath = download_txt(url, 'Али\\би', folder='txt/')
        self.assertEqual(filepath, 'txt/Алиби.txt')


if __name__ == "__main__":
    unittest.main()
