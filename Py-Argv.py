from enum import Enum
from typing import List
from dataclasses import dataclass
from re import findall
class ArgvType(Enum):
    Switch = 1
    Key = 2
@dataclass(frozen=True)
class Argv:
    type: ArgvType
    name: str
def scan(argv: str, target: List[Argv], switch_code="--", key_code="-"):
    args = findall(r'[^\s"]+|".+?"', argv)
    result = {a.name:(False if a.type == ArgvType.Switch else None) for a in target}
    used_switches = [temp for temp in filter(lambda a: a.type == ArgvType.Switch, target) if switch_code + temp.name in args]
    for switch in used_switches:
        result[switch.name] = True
        args.remove(switch_code + switch.name)
    for key in [__k for __k in filter(lambda a: a.type == ArgvType.Key, target) if key_code + __k.name in args]:
        result[key.name] = eval(args[args.index(key_code + key.name) + 1].replace("\\", "\\\\"))
    return result

if __name__ == "__main__":
    print(scan("--noConsole -ico \"C:\\Users\\user\\Desktop\\icon.ico\" -name \"MyFirstProject Season II\" -version 3", \
        [Argv(ArgvType.Switch, "noConsole"), Argv(ArgvType.Key, "ico"), Argv(ArgvType.Key, "name"), Argv(ArgvType.Key, "version")]))