from sqlalchemy.orm import declarative_base


class CustomBase:
    def dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns  # type: ignore
        }


Base = declarative_base(cls=CustomBase)
