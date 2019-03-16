from .say      import say
from .store    import store
from .top      import top
from .activity import activity
from .unknown_command import unknown_command


identifiers = {
    "say":   say,
    "store": store,
    "top":   top,
    "activity": activity,
    "unknown_command": unknown_command
}
