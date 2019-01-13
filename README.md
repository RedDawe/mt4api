# mt4api

This code is based mainly on https://www.youtube.com/watch?v=GldkyrvbIQw, https://www.youtube.com/watch?v=_-NsIIsdFGM&t=273s, https://mql4tradingautomation.com/mql4-calculate-position-size/ and https://www.mql5.com/en/forum/108872.
(and random sites on the internet)

Also see the videos for installation

My code is merely and update to the original code in the videos, but natively supports multiple instruments (closing  orders), automates lots sizing based on percentage risk (be careful if MarketInfo(pair, MODE_TICKVALUE) returns the correct value with your broker), allows you to exctract information about your account balance and open orders on a specific pair, repairs timeframes and pulls High and Low prices together with Close.

The code is not commented (there are the original comments before my edit), but I think the changes are pretty self-explainatory.
Also, the code doesn't check for errors.

The only thing that I would mention, is that stop loss is passed as price, not in pips.

The code is not properly tested, so use on your own danger and don't blame me for your lost money.

On the other side, if you find any bugs in there, it would be heavily appreciated if you let me know.

contact: davorak01@gmail.com
