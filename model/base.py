from sqlalchemy import MetaData, create_engine
from sqlobject import (
    RelatedJoin,
    SingleJoin,
    SQLObject,
    IntCol,
    FloatCol,
    MultipleJoin,
    ForeignKey,
    StringCol,
    TimeCol,
    connectionForURI,
    sqlhub
)

from time import time

from sqlobject.dberrors import OperationalError

import logging

logging.basicConfig(
    filename='test.log',
    format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
    level=logging.DEBUG,
)

log = logging.getLogger("TEST")

log.info("Log started")

__connection__ = "sqlite:splits.sqlite?debug=1&logger=TEST&loglevel=debug"

sqlhub.processConnection = connectionForURI(__connection__)


class Game(SQLObject):
    game_name = StringCol()
    splits = MultipleJoin('Split')
    ui = SingleJoin('ConfigUserInterface')


class ConfigUserInterface(SQLObject):
    game = ForeignKey('Game')
    r_bg_color = IntCol()
    g_bg_color = IntCol()
    b_bg_color = IntCol()
    alpha_level = FloatCol()


class Split(SQLObject):
    game = ForeignKey('Game')
    split_time = TimeCol()


if __name__ == "__main__":
    try:
        Split.dropTable(cascade=True)
        Game.dropTable(cascade=True)
        ConfigUserInterface.dropTable(cascade=True)
    except OperationalError:
        pass

    try:
        Game.createTable()
        Split.createTable()
        ConfigUserInterface.createTable()
    except OperationalError:
        pass

    darksouls3 = Game(game_name="Dark Souls III")

    split1 = Split(
        game=darksouls3,
        split_time=time(hour=0, minute=13, second=10)
    )

    split2 = Split(
        game=darksouls3,
        split_time=time(hour=0, minute=32, second=20)
    )

    split3 = Split(
        game=darksouls3,
        split_time=time(hour=0, minute=44, second=30)
    )

    split4 = Split(
        game=darksouls3,
        split_time=time(hour=0, minute=54, second=40)
    )

    cui = ConfigUserInterface(
        game=darksouls3,
        r_bg_color=42,
        g_bg_color=42,
        b_bg_color=42,
        alpha_level=.5
    )

    Game._connection.debug = True
    ConfigUserInterface._connection.debug = True
    Split._connection.debug = True

    g = Game.get(1)
    print(f"RGB=({g.ui.r_bg_color}, {g.ui.g_bg_color}, {g.ui.b_bg_color})")
    print(f"alpha={g.ui.alpha_level}")

    for s in g.splits:
        print(s.split_time)
