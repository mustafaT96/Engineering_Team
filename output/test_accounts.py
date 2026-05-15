import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('test_user', 10000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 10000.0)

    def test_deposit(self):
        self.account.deposit(5000.0)
        self.assertEqual(self.account.balance, 15000.0)

    def test_withdraw_success(self):
        self.account.withdraw(1000.0)
        self.assertEqual(self.account.balance, 9000.0)

    def test_withdraw_failure(self):
        result = self.account.withdraw(20000.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertEqual(self.account.holdings['AAPL'], 10)

    def test_buy_shares_failure(self):
        self.account.withdraw(5000.0)  # Make balance low
        result = self.account.buy_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertNotIn('AAPL', self.account.holdings)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(self.account.balance, 9250.0)

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 5)
        self.assertFalse(result)
        self.assertEqual(self.account.holdings['AAPL'], 10)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 10)
        self.assertEqual(self.account.calculate_portfolio_value(), 8500.0 + 1500.0)

    def test_calculate_profit_or_loss(self):
        self.assertEqual(self.account.calculate_profit_or_loss(), 0.0)

    def test_list_holdings(self):
        self.account.buy_shares('AAPL', 10)
        self.assertEqual(self.account.list_holdings(), {'AAPL': 10})

    def test_list_transactions(self):
        self.account.buy_shares('AAPL', 10)
        self.assertEqual(len(self.account.list_transactions()), 1)

if __name__ == '__main__':
    unittest.main()