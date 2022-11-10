# Assignment 3. Programming of Intelligent Information Systems course

### Project Structure

 1. NegaMax
 2. NegaScout
 3. PVS

## 0. Evaluation Function

For all our algorithm implementations, we need evaluation function to estimate the value or goodness of a position (usually at a leaf or terminal node) in a game tree.

In our case, we depend on positions number of white/black pieces and material balance of the board.

```
    def material_balance(self, board, white, black):
        return (
                chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )
```


Read more about material balance in the chess [here](https://www.chess.com/article/view/the-evaluation-of-material-imbalances-by-im-larry-kaufman).
Now, let's declare some constants.

## 1. NegaMax Implementation

- it is a variant of MiniMax;
- the value of a given position to the first player is a negation of the value to the second player;
- each player looks for a move that will maximise the damage to the opponent;

![img.png](img.png)

## 2. NegaScout Implementation

Like NegaMax but improvements rely on NegaMax framework and some fail-soft issues concerning the two last plies, which did not require any re-searches.

- Idea: search first move fully to establish a lower bound
- Null window search to try to prove that other moves have
score <= v
- If fail high, re-search to establish exact score of new, better
move
- With good move ordering, re-search rarely needed. Savings
from using null window outweigh cost of re-search

NegaScout's fail-soft refinements always returns correct minimax scores at the two lowest levels, since it assumes that all horizon nodes would have the same score 
for the (in that case redundant) re-search, which most programs can not guarantee due to possible extensions 
and possible bound dependency of quiescence search and evaluation. 
NegaScout just searches the first move with an open window, and then every move after that with a zero window, whether alpha was already improved or not. 
Some PVS implementations wait until an alpha-improvement before using zero window at PV-Nodes.

A Null Window, also called Zero Window, Scout Window or Narrow Window, is a way to reduce the search space in alpha-beta like search algorithms, to perform a boolean test, whether a move produces a worse or better score than a passed value. 

## 3. Principal variation search

Very similar to NegaScout Algorithm.

The difference is how they handle re-searches: PVS passes alpha/beta while NegaScout passes the value returned by the null window search instead of alpha. 
But then you can get a fail-low on the research due to search anonomalies. If that happens NegaScout returns the value from the first search. 
That means you will have a crippled PV. Then there is a refinement Reinefeld suggests which is to ommit the re-search at the last two plies (depth > 1) - but that won't work in a real program because of search extensions. 
NegaScout is slightly an ivory tower variant of PVS (IMHO).

## 4. Game Engine
Let's request which algorithm implementation we want to test.

In case of invalid input, there will be exception raised.

After that, we implement game simulation with the user.