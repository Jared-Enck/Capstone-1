
# DCG-Tamer  

Deployed on Heroku: https://dcg-tamer.herokuapp.com/  

## Description  

A site to look up cards and build decks for the Digimon Card Game series. Which has become a very popular trading card game (TCG) by Bandai, since it's revamp in 2020.  

# Features  

## Search Cards  

User will be able to search/view cards through regular and advanced search. Advanced search will have filter options.  

## Create Account/Login  

Logged in users will have access to the deckbuilder, share deck, and like deck features.  

## Deckbuilder  

Here a user can build a deck by using the advanced search to call the API and click to add the cards to their main deck, egg deck, or side decks.

Then name and save the deck.

## Share/Delete  

Logged in users that own the deck, on the deck details page, can share the deck for all to see or delete their deck.  

## Likes  

Logged in users that do not own the deck, on the deck details page, can click the like button to add a like to the deck. This will also add the deck to the logged in user's liked decks page.

If already liked, this will remove a like from and remove the deck from the logged in user's liked decks page.  

## Liked Decks  

On the user profile page, there will be a link to the liked decks. Here a user will see the profile user's liked decks.

# User Flow  

Created with Lucidchart.  

![DCG-Tamer user flow](/DCG-Tamer_user-flow.png)  

#  API Notes  

URL: https://documenter.getpostman.com/view/14059948/TzecB4fH#5d82e651-26d7-4c58-8b9a-f021f5cc1dfd  

The API is pretty straight foward with only two endpoints. One for getting all cards and the other for getting cards by name, or other params.  

It does have a rate limit of fifteen calls per ten seconds. So it was fine for searching cards (with low user base). However, I was unable to use it for getting all cards in a deck. So I ended up saving all the cards from the series I used for this site in my seed file. This way I could just pull the card info for the cards needed from my database.

# Database Schema  

Created with Quick DBD.

![DCG-Tamer schema](/DCG_Tamer_schema.png)  

# Technology Stack

## Front End  

| HTML5 | CSS | JavaScript | Bootstrap | jQuery |
| ----- | ----- | ----- | ----- | ----- |
| ![html5 icon](https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/html-5.svg) | ![css icon](https://github.com/get-icon/geticon/raw/master/icons/css-3.svg) | ![javascript icon](https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/javascript.svg) | ![bootstrap icon](https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/bootstrap.svg) | ![jquery icon](https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/jquery-icon.svg) |

## Back End

| Python3 | PostgreSQL | Flask |
| ----- | ----- | ----- |
| ![python icon](https://github.com/get-icon/geticon/raw/master/icons/python.svg) | ![postgresql icon](https://github.com/get-icon/geticon/raw/master/icons/postgresql.svg) | ![flask icon](https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/flask.svg) |

Icons obtained from https://github.com/get-icon/geticon