# **trading_bot**

This is the beginning of a major project.

I had a trading strategy that I wanted to test, so I decided to make a program. I chose python because I was curious about it.

The result was that I was a better choice to code the program entirelly using mql4 (it's a language so similar to C) because that way I had also trading functions to make Orders DIRECTLY in the market.

Despite that, the main point of the strategy is here, in python.

### Details of the strategy implemented

- Considering two 'big pivots', I make a trend.
  >> What 'big pivots' are: a big top pivot has four lower candles before and after itself. For a bot pivot, it's the opposite.
- If the market price breaks the trend done by those two big pivots, it's the start of a signal.
- The entry point is in the closest big pivot.

NOTE: This strategy has more variables, it doesn't work well with only this conditions. But I think it's a curious project to make it public.

Hope anyone interested on doing this kind of thing could take value from this repo.
