import unittest
import requests
from unittest.mock import patch, Mock
from scrapper.page_fetcher import PageFetcher
from exceptions.network_error import NetworkError

class TestPageFetcher(unittest.TestCase):
    
    def setUp(self):
        self.fetcher = PageFetcher("https://dentalstall.com/shop/", "http://193.29.63.45:8080")

    @patch('requests.get')
    def test_fetch_page_success(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_page(1)
        self.assertEqual(result, "<html></html>")
        mock_get.assert_called_once_with("https://dentalstall.com/shop/", proxies={'http': 'http://193.29.63.45:8080'})

if __name__ == '__main__':
    unittest.main()
