import gradio as gr
from accounts import Account, get_share_price

account = {"obj": None}


def create_account(username, initial_deposit):
    if not username:
        return "Please enter a username."
    try:
        initial_deposit = float(initial_deposit)
    except (ValueError, TypeError):
        return "Please enter a valid initial deposit amount."
    account["obj"] = Account(username, initial_deposit)
    return f"Account created for {username} with initial deposit ${initial_deposit:.2f}"


def deposit_funds(amount):
    if account["obj"] is None:
        return "Please create an account first."
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return "Please enter a valid amount."
    if amount <= 0:
        return "Amount must be positive."
    account["obj"].deposit(amount)
    return f"Deposited ${amount:.2f}. New balance: ${account['obj'].balance:.2f}"


def withdraw_funds(amount):
    if account["obj"] is None:
        return "Please create an account first."
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return "Please enter a valid amount."
    if amount <= 0:
        return "Amount must be positive."
    success = account["obj"].withdraw(amount)
    if success:
        return f"Withdrew ${amount:.2f}. New balance: ${account['obj'].balance:.2f}"
    return "Insufficient balance for withdrawal."


def buy_shares(symbol, quantity):
    if account["obj"] is None:
        return "Please create an account first."
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return "Please enter a valid quantity."
    if quantity <= 0:
        return "Quantity must be positive."
    symbol = symbol.upper().strip()
    price = get_share_price(symbol)
    if price == 0.0:
        return f"Unknown symbol: {symbol}. Try AAPL, TSLA, GOOGL."
    success = account["obj"].buy_shares(symbol, quantity)
    if success:
        return f"Bought {quantity} shares of {symbol} at ${price:.2f} each. Balance: ${account['obj'].balance:.2f}"
    return "Insufficient funds to buy shares."


def sell_shares(symbol, quantity):
    if account["obj"] is None:
        return "Please create an account first."
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return "Please enter a valid quantity."
    if quantity <= 0:
        return "Quantity must be positive."
    symbol = symbol.upper().strip()
    price = get_share_price(symbol)
    if price == 0.0:
        return f"Unknown symbol: {symbol}. Try AAPL, TSLA, GOOGL."
    success = account["obj"].sell_shares(symbol, quantity)
    if success:
        return f"Sold {quantity} shares of {symbol} at ${price:.2f} each. Balance: ${account['obj'].balance:.2f}"
    return "You don't have enough shares to sell."


def show_holdings():
    if account["obj"] is None:
        return "Please create an account first."
    holdings = account["obj"].list_holdings()
    if not holdings:
        return "No holdings."
    rows = [f"{sym}: {qty} shares (current price ${get_share_price(sym):.2f})" for sym, qty in holdings.items()]
    return "\n".join(rows)


def show_portfolio():
    if account["obj"] is None:
        return "Please create an account first."
    value = account["obj"].calculate_portfolio_value()
    pl = account["obj"].calculate_profit_or_loss()
    return (
        f"Cash balance: ${account['obj'].balance:.2f}\n"
        f"Total portfolio value: ${value:.2f}\n"
        f"Profit/Loss: ${pl:.2f}"
    )


def show_transactions():
    if account["obj"] is None:
        return "Please create an account first."
    txs = account["obj"].list_transactions()
    if not txs:
        return "No transactions yet."
    lines = []
    for i, t in enumerate(txs, 1):
        lines.append(f"{i}. {t['type'].upper()} {t['quantity']} {t['symbol']} @ ${t['price']:.2f}")
    return "\n".join(lines)


with gr.Blocks(title="Trading Simulation Account") as demo:
    gr.Markdown("# Trading Simulation Account Demo")
    gr.Markdown("Available symbols: **AAPL** ($150), **TSLA** ($750), **GOOGL** ($2800)")

    with gr.Tab("Create Account"):
        username = gr.Textbox(label="Username")
        initial_deposit = gr.Number(label="Initial Deposit", value=10000)
        create_btn = gr.Button("Create Account")
        create_out = gr.Textbox(label="Result")
        create_btn.click(create_account, [username, initial_deposit], create_out)

    with gr.Tab("Deposit / Withdraw"):
        with gr.Row():
            with gr.Column():
                dep_amt = gr.Number(label="Deposit Amount", value=0)
                dep_btn = gr.Button("Deposit")
                dep_out = gr.Textbox(label="Result")
                dep_btn.click(deposit_funds, dep_amt, dep_out)
            with gr.Column():
                wd_amt = gr.Number(label="Withdraw Amount", value=0)
                wd_btn = gr.Button("Withdraw")
                wd_out = gr.Textbox(label="Result")
                wd_btn.click(withdraw_funds, wd_amt, wd_out)

    with gr.Tab("Buy / Sell Shares"):
        with gr.Row():
            with gr.Column():
                buy_sym = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Symbol", value="AAPL")
                buy_qty = gr.Number(label="Quantity", value=1, precision=0)
                buy_btn = gr.Button("Buy")
                buy_out = gr.Textbox(label="Result")
                buy_btn.click(buy_shares, [buy_sym, buy_qty], buy_out)
            with gr.Column():
                sell_sym = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Symbol", value="AAPL")
                sell_qty = gr.Number(label="Quantity", value=1, precision=0)
                sell_btn = gr.Button("Sell")
                sell_out = gr.Textbox(label="Result")
                sell_btn.click(sell_shares, [sell_sym, sell_qty], sell_out)

    with gr.Tab("Reports"):
        with gr.Row():
            holdings_btn = gr.Button("Show Holdings")
            portfolio_btn = gr.Button("Show Portfolio Value & P/L")
            tx_btn = gr.Button("Show Transactions")
        report_out = gr.Textbox(label="Report", lines=10)
        holdings_btn.click(show_holdings, None, report_out)
        portfolio_btn.click(show_portfolio, None, report_out)
        tx_btn.click(show_transactions, None, report_out)


if __name__ == "__main__":
    demo.launch()