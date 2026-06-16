╔══════════════════════════════════════════════════════════════╗
║           CAR RACING GAME — 10 Levels                        ║
╚══════════════════════════════════════════════════════════════╝

REQUIREMENTS
  Python 3.13+  |  pip install pygame

HOW TO RUN
  1.  pip install pygame
  2.  python3 generate_assets.py    (only once, creates assets/)
  3.  python3 game.py

CONTROLS
  ← / A      Move car left
  → / D      Move car right
  ENTER      Start / Next level
  R          Restart from Level 1
  ESC        Quit

══════════════════════════════════════════════════════════════
 #   Level Name          Enemies  Background
══════════════════════════════════════════════════════════════
 1   City Highway           1     Daytime city with buildings
 2   Night Desert           2     Dark desert with cacti & moon
 3   Countryside            2     Green fields, trees, blue sky
 4   Snow Storm             3     White snowfall, pine trees
 5   Sunset Boulevard       3     Orange sky, palm silhouettes
 6   Rainy Night City       4     Neon reflections in the rain
 7   Mountain Pass          4     Snowy peaks, rocky terrain
 8   Neon Tunnel            5     Underground neon light strips
 9   Dusk Bridge            5     Bridge over water at sunset
10   Space Highway          6     Stars, nebula, glowing road
══════════════════════════════════════════════════════════════

TIPS
  • Each level has a score GOAL shown in the progress bar
  • Coins give +50 bonus score
  • You start with 3 lives (4 from Lv5, 5 from Lv8)
  • After a hit you briefly blink — invincible during that time
  • Speed increases over time; enemy count grows too
  • Dying returns you to Level 1

FILES
  game.py              Main game (Python 3.13+)
  generate_assets.py   Generate all PNG assets (run once)
  assets/              All images (auto-created)
