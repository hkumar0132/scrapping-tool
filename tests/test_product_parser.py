import unittest
from scrapper.product_parser import ProductParser
from exceptions.parsing_error import ParsingError

class TestProductParser(unittest.TestCase):

    def test_parse_products_with_valid_input(self):
        mock_html = """
        <div class="product">
            <h2 class="woo-loop-product__title">Sample Product</h2>
            <span class="price">
                <ins><span class="woocommerce-Price-amount amount">₹885.00</span></ins>
                <del><span class="woocommerce-Price-amount amount">₹960.00</span></del>
            </span>
            <img data-lazy-src="https://dentalstall.com/wp-content/uploads/2023/03/minipex8-300x300.jpg" />
        </div>
        """
        
        products = ProductParser.parse_products(mock_html)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].product_title, "Sample Product")
        self.assertEqual(products[0].product_price, 885.00)
        self.assertEqual(products[0].path_to_image_public, "https://dentalstall.com/wp-content/uploads/2023/03/minipex8-300x300.jpg")

    def test_parse_products_with_missing_title(self):
        mock_html = """
        <div class="product">
            <span class="price">
                <ins><span class="woocommerce-Price-amount amount">₹885.00</span></ins>
                <del><span class="woocommerce-Price-amount amount">₹960.00</span></del>
            </span>
            <img data-lazy-src="https://dentalstall.com/wp-content/uploads/2023/03/minipex8-300x300.jpg" />
        </div>
        """
        with self.assertLogs('scrapper.product_parser', level='WARNING') as log:
            products = ProductParser.parse_products(mock_html)
            self.assertEqual(products, [])
            self.assertIn("Product title not found", log.output[0])

    def test_parse_products_with_invalid_price_format(self):
        mock_html = """
        <div class="product">
            <h2 class="woo-loop-product__title">Sample Product</h2>
            <span class="price">
                <span class="woocommerce-Price-amount amount">Not a Price</span>
            </span>
            <img data-lazy-src="https://dentalstall.com/wp-content/uploads/2023/03/minipex8-300x300.jpg" />
        </div>
        """
        with self.assertRaises(ParsingError) as context:
            ProductParser.parse_products(mock_html)
        self.assertIn("Invalid price format encountered", str(context.exception))

    def test_parse_products_with_no_products(self):
        mock_html = "<div></div>"
        products = ProductParser.parse_products(mock_html)
        self.assertEqual(products, [])

if __name__ == '__main__':
    unittest.main()
