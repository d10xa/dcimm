from dataclasses import dataclass


@dataclass(frozen=True)
class LocalDateTime:
    year: str
    month: str
    day: str
    hour: str
    minute: str
    second: str

    def yyyymmdd(self):
        return f'{self.year}-{self.month}-{self.day}'

    def yyyymm(self):
        return f'{self.year}-{self.month}'
