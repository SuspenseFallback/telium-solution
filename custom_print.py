import time
import sys

def custom_print(*args, sep=" ", end="\n"):
    joined = sep.join([str(i) for i in args])
    for i in range(0, len(joined) - 1):
        print(joined[i], end="", flush=True)
        time.sleep(0.02)

    print(joined[-1], end=end)