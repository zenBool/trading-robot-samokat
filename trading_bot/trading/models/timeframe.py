from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from trading.enums import enums


def check_name(v: str) -> str:
    assert v in enums.TIMEFRAMES.keys(), f'{v} is invalid interval name'
    return v


class Timeframe(BaseModel):
    name: Annotated[str, AfterValidator(check_name)]

    @property
    def ms(self):
        return enums.TIMEFRAMES[self.name]

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, ms={self.ms})'


if __name__ == '__main__':
    i = Timeframe(name='1m')
    print(i.__repr__())
    print(i.name)
    print(i.ms)


