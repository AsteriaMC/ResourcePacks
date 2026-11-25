import argparse

from . import commands  # noqa: F401  (imports all commands so they register)
from .core.command import execute, list_commands, valid_args, script_exists


def main():
    parser = argparse.ArgumentParser(description="Run a registered script command.")
    parser.add_argument("command", nargs="?", help="The script command to run.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the command.")

    parsed = parser.parse_args()

    if not parsed.command:
        list_commands()
    else:
        # split so that
        # --key=value -> key="value"
        # --key value -> key="value"
        # --flag      -> flag=True
        pos_args = []
        kwargs = {}
        tokens = parsed.args
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("--"):
                key, has_eq, val = token[2:].partition("=")
                if not has_eq:
                    next_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                    if next_tok is not None and not next_tok.startswith("--"):
                        val = next_tok
                        i += 1
                    else:
                        val = True
                kwargs[key.replace("-", "_")] = val
            else:
                pos_args.append(token)
            i += 1

        if not script_exists(parsed.command):
            print(f"Error: {parsed.command} not a command!")
        elif not valid_args(parsed.command, *pos_args, **kwargs):
            print(f"Error: {parsed.command} too many or too little args")
        else:
            execute(parsed.command, *pos_args, **kwargs)


if __name__ == "__main__":
    main()
