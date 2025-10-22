# Omnibus Rook

The project includes two games using Rook cards, the first is what I call "Omnibus Rook", because it combines the rules of three versions of Rook: The [Original Rules](https://www.rookcards.com/Pictures/RuleBooks/RB086/RB086.pdf), the standard tournament rules, and the Red One variation, which adds a special "Red One" card worth 30 points. This variation uses a 58 card deck of 4 suits of 14 cards, plus the Rook card and Red One. This is a cutthroat variation where each player scores points for themselves.

As of now there is no bidding, and the player chooses trump for each round.

## Golden 10

This repo also includes an implementation of Golden 10, a Hearts-like game played with Rook cards. Each red card is worth 1 point, except for the red 5 worth 5 points, and the red 10 card worth 10 points, and the yellow 10 subtracts 10 points from your score. The goal is to lowest score at the end of the round.

The above two games were written in Python using [pyglet](https://pyglet.org/).

## Sources

The card images and background are from [Nathan Friend's PHP Websockets project](https://github.com/nfriend/Rook), and the trump picker is from the [Parker Brothers Classic Card Games CD-ROM](https://archive.org/details/PBCLASSIC).

