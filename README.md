# QF205

This is an alternative snake game for module QF205 using 'python' and 'Pygame'
The game was made as a sketch to assist in a report for teaching the basics of the Python 3.x language

## Controls

|              | Button              |
|--------------|---------------------|
| Move Left    | <kbd>←</kbd>        |
| Move right   | <kbd>→</kbd>        |
| Move up      | <kbd>↑</kbd>        |
| Move down    | <kbd>↓</kbd>        |
| Quit game    | <kbd>esc</kbd>      |

## Instructions

### For both 'Windows' and 'MAC OS'
```
- Extract files anywhere and open the 'cmd' or 'terminal' respectively in the PythonZ folder
- ~/PythonZ> python main.py
```

## Warning
The code below is included due to simplicity and is never recommended for future use.
Dependencies should always be managed externally.
```python
try:
    import pygame
except ImportError:
    print("Missing pygame. Attempting to install...")
    os.system("python -m pip install pygame")
import pygame
```