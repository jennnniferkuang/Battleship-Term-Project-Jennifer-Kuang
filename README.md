# Battleship Term Project Jennifer Kuang
 
***What's in this repo so far:***
- Asset folder containing:
    - 2 planes, 1 for each opposing side
    - 8 ships, 4 for each opposing side
- Python file containing all code so far (see 'code' section)
- This readme file
- A gitattributes file that has absolutely no use to me

**Assets:**
- All battleship/plane assets are illustrated by my friend. His Instagram is 
    @gawain_draws. All assets are paid for, with all rights to personal use 
    given to me as the commissioner. As of now these are the only assets I have.

**Code:**
- Ship class (need 8 total, likely need to relate to grids in a way)
- Grid class (need 2 for game)

**To Do:**
- How to change app.width/height to screen width/height or let user choose
- check to make sure computer's selected ship locations do not overlap. (Change to row, col generation instead?)
- implement rotate ship
- draw states of ships/guess
- something buggy about guess dot

**Dev Only:**
# Official MVP Definition
Code Organization:
- An outside user can understand the code and what is being written
- Student displays knowledge of style learned throughout the semester

User Interface (UI): 
- Decent game interface
- Representations for bombs and ships

User Experience (UX):
- Board contains all properties
- Ships can legally placed around the board
- All game rules implemented including:
    - Placing ships
    - Bombing ships 
    - When the ship die

Algorithmic Complexity: 
- OOP 
    - Keeps track of all cell status & ships
- Game AI Opponent
    - Before game: Being able to put in different ships every round
    - During game: Being able to select cell to bomb with some sort of thinking 