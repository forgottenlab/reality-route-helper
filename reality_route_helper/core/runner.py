import subprocess
from dataclasses import dataclass
from typing import List


@dataclass
class CommandResult:
    code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.code == 0

    @property
    def text(self) -> str:
        return "\n".join(x for x in [self.stdout, self.stderr] if x)


def run(cmd: List[str], timeout: int = 30) -> CommandResult:
    try:
        proc = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())
    except Exception as exc:
        return CommandResult(1, "", str(exc))
