from .say      import say
from .store    import store
from .top      import top
from .activity import activity
from .help     import help
from .thank    import thank
from .unknown_command import unknown_command


identifiers = {
    "say":   say,
    "store": store,
    "top":   top,
    "activity": activity,
    "help": help,
    "thank": thank,
    "unknown_command": unknown_command
}
