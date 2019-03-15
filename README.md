# QF205

This is an alternative snake game for module QF205 using 'python' and 'Pygame'
The game was made as a sketch to assist in a report for teaching the basics of the Python 3.x language

## Controls

|              | Button              |
|--------------|---------------------|
| Move Left    | <kbd>left</kbd>     |
| Move right   | <kbd>right</kbd>    |
| Move up      | <kbd>up</kbd>       |
| Move down    | <kbd>down</kbd>     |
| Quit game    | <kbd>Esc</kbd>      |

## Instructions

### For both 'Windows' and 'MAC OS'
```bash
- Extract files anywhere and open the 'cmd' or 'terminal' respectively in the PythonZ folder
- ~/PythonZ> python main.py
```

## Warning
The code below is included and is never recommended for future use.
Dependencies should always be managed externally.
```python
try:
    import pygame
except ImportError:
    print("Missing pygame. Attempting to install...")
    os.system("python -m pip install pygame")
import pygame
```