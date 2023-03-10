import datetime
from collections.abc import Generator

from state_script import State, JsonFileStorage


def load_from_postgres(batch: Generator, cursor_pg, table):
    state = State(JsonFileStorage('.'))
    try:
        time = datetime.datetime.fromisoformat(state.get_state(table))
    except TypeError:
        time = datetime.datetime(
            1000, 1, 16, 20, 14, 9, 222485, tzinfo=datetime.timezone.utc)
    # ПОЛУЧАЕМ ВСЮ ИНФУ ДЛЯ ЗАПИСИ В ЭЛАСТИК
    last_modified = datetime.datetime(1000, 1, 16)

    if table == 'content.genre':
        cursor_pg.execute(
            f"""
                    SELECT id, name, updated_at
                    FROM {table}
                    WHERE updated_at > '{time}'
                    ORDER BY updated_at
                    ;
                    """
        )
    while True:
        size = 50
        try:
            entries = cursor_pg.fetchmany(size)
        except BaseException:
            break
        if len(entries) == 0 or entries is None:
            # дата изменения последней отправленной в ETL записи, отличная от
            # 1000-01-16 00:00:00 - гарантия того, что изменения были
            if str(last_modified) != '1000-01-16 00:00:00':
                state.set_state(table, str(last_modified))
            break
        else:
            last_modified = entries[-1][2]
            data_list = entries
            print(data_list)
            batch.send(data_list)
