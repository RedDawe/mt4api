import zmq
import numpy as np

timeframes = {
    'm1': '1',
    'm5': '5',
    'm15': '15',
    'm30': '30',
    'H1': '60',
    'H4': '240',
    'D1': '1440',
    'W1': '10080',
    'M1': '43200'
}

class zmq_python():
    def __init__(self):
        # Create ZMQ Context
        self.context = zmq.Context()

        # Create REQ Socket
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect("tcp://localhost:5555")

        # Create PULL Socket
        self.pullSocket = self.context.socket(zmq.PULL)
        self.pullSocket.connect("tcp://localhost:5556")

    def remote_send(self, socket, data):

        try:
            socket.send_string(data)
            msg_send = socket.recv_string()
            print(msg_send)

        except zmq.Again as e:
            print("Waiting for PUSH from MetaTrader 4..")

    def remote_pull(self, socket):

        try:
            msg_pull = socket.recv(flags=zmq.NOBLOCK)
            return msg_pull

        except zmq.Again as e:
            print("Waiting for PUSH from MetaTrader 4..")

    def get_data(self, symbol, timeframe, end_bar, include_uncompleted_candle = True, start_bar = 0):
        '''
        only start_bar and end_bar as int

        end_bar == number of returned elements if uncompleted candle is being returned
        else end_bar -1

        '''
        self.data = "DATA|" + symbol + "|" + timeframes[timeframe] + "|" + str(start_bar) + "|" + str(end_bar)
        self.remote_send(self.reqSocket, self.data)
        prices = self.remote_pull(self.pullSocket)
        prices_str = str(prices)

        price_lst = prices_str.split(sep='|')[1:]
        price_lst[-1] = price_lst[-1][:-1]

        price_lst = [float(i) for i in price_lst]
        price_lst = price_lst[::-1]

        price_arr = np.array(price_lst).reshape(3, -1)

        if not include_uncompleted_candle:
            price_arr = price_arr[:, :-1]

        return price_arr

        # high
        # low
        # close

    def buy_order(self, symbol, stop_loss, take_profit = 0):
        self.buy = "TRADE|OPEN|1|" + str(symbol) + "|" + str(stop_loss) + "|" + str(take_profit)
        self.remote_send(self.reqSocket, self.buy)
        reply = self.remote_pull(self.pullSocket)
        return reply

    def sell_order(self, symbol, stop_loss, take_profit = 0):
        self.sell = "TRADE|OPEN|0|" + str(symbol) + "|" + str(stop_loss) + "|" + str(take_profit)
        self.remote_send(self.reqSocket, self.sell)
        reply = self.remote_pull(self.pullSocket)
        return reply

    def close_orders(self, symbol):
        self.close = "TRADE|CLOSE|" + str(symbol)
        self.remote_send(self.reqSocket, self.close)
        reply = self.remote_pull(self.pullSocket)
        return reply

    def open_state(self, symbol):
        self.open = "STATE|0|" + symbol
        self.remote_send(self.reqSocket, self.open)
        reply = self.remote_pull(self.pullSocket)
        return int(str(reply)[2:-1])

        """
        if state == -1:
            print('Open sell order')
        if state == 0:
            print('No open orders')
        if state == 1:
            print('Open buy order')
        """

    def acc_balance(self):
        self.balance = "STATE|1"
        self.remote_send(self.reqSocket, self.balance)
        reply = self.remote_pull(self.pullSocket)
        return float(str(reply)[2:-1])