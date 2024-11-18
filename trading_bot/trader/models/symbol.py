from pydantic import BaseModel


class Symbol(BaseModel):
    name: str

    def lower(self):
        return self.name.lower()

    def __str__(self):
        return f'{self.name}'


if __name__ == '__main__':
    s = Symbol(name='BTCUSDT')
    print(s.name)
    print(s)
