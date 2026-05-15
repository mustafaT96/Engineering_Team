class Account:
    def __init__(self, username: str, initial_deposit: float) -> None:
        self.username = username
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            transaction = {'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price}
            self.transactions.append(transaction)
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = get_share_price(symbol)
            total_earnings = price * quantity
            self.balance += total_earnings
            self.holdings[symbol] -= quantity
            transaction = {'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': price}
            self.transactions.append(transaction)
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, shares in self.holdings.items():
            total_value += get_share_price(symbol) * shares
        return total_value

    def calculate_profit_or_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def list_holdings(self) -> dict:
        return self.holdings

    def list_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 750.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)


# Example test
test_account = Account('test_user', 10000.0)
test_account.deposit(5000.0)
test_account.buy_shares('AAPL', 10)
test_account.sell_shares('AAPL', 5)
test_account.withdraw(1000.0)
portfolio_value = test_account.calculate_portfolio_value()
profit_or_loss = test_account.calculate_profit_or_loss()
print(portfolio_value, profit_or_loss, test_account.list_holdings(), test_account.list_transactions())