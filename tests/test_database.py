import sys

import pytest

if 'database' in sys.modules:
    del sys.modules['database']

from database import Database


@pytest.fixture
def db():
    database = Database(':memory:')
    return database


def test_create_table(db):
    db.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='groups_info'"
    )
    assert db.cursor.fetchone() is not None


def test_add_group(db):
    chat_id = 12345
    group_name = 'Test Group'

    db.add_group(chat_id, group_name)

    data = db.get_group_data(chat_id)
    assert data is not None
    assert data['chat_id'] == chat_id
    assert data['group_name'] == group_name
    assert data['mat_counter'] == 0
    assert data['bot_switch'] == 1
    assert data['ban_list'] == []
    assert data['ban_words'] == []


def test_add_existing_group(db):
    chat_id = 12345
    db.add_group(chat_id, 'Group 1')

    db.set_bot_switch(chat_id, 0)

    db.add_group(chat_id, 'Group 1')

    data = db.get_group_data(chat_id)
    assert data['bot_switch'] == 1


def test_update_ban_list(db):
    chat_id = 12345
    db.add_group(chat_id, 'Test')

    new_ban_list = ['bad_user']
    db.update_ban_list(chat_id, new_ban_list)

    data = db.get_group_data(chat_id)
    assert 'bad_user' in data['ban_list']


def test_increment_mat_counter(db):
    chat_id = 12345
    db.add_group(chat_id, 'Test')

    db.increment_mat_counter(chat_id)
    db.increment_mat_counter(chat_id)

    data = db.get_group_data(chat_id)
    assert data["mat_counter"] == 2
