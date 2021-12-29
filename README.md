# the_equilator
Fast python poker hands evaluator (using numpy/numba).

This is my first python program (written at the very beginning of my career).<br>
But it still works very fast and can be useful for creating a poker engine using Python

<b>How to:</b>
<ul>1. git clone repository</ul>
<ul>2. install requirements.txt</ul>
<ul>3. correct values if necessary in <b>main.py</b> (read some instructions there)</ul>
<ul>4. run <b>main.py</b></ul>

<b>Features:</b>

<ul>1. Weighted input is supported.</ul>
<ul>2. You can get not only the total equity of the ranges, but the equity of absolutely all hands in the range separately.</ul>
<ul>3. Calculations with weigths are 3x+ times faster than Equilab from pokerstrategy.com (even w/o weigths)</ul>
<ul>4. numba nJIT optimizes the code for the specific processor on which it runs, often surpasses the speed of python C-function calls. </ul>
If you want to use this software for commercial purposes (to create a solver / engine / bot), I would prefer to be informed at silentvik@gmail.com.<br>
In addition, I can help (all of the above has already been created, also obviously not the most optimized version is presented here).
