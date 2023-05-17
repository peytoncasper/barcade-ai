import uuid

import psycopg2
import os

connection_config = {
    'host': os.environ["DB_IP"],
    'database': "postgres",
    'user': os.environ["DB_USERNAME"],
    'password': os.environ["DB_PASSWORD"]
}

def deactivate_game(game_id):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET active = %s
        WHERE id = %s
    """
    cursor.execute(query, (False, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_one_score(game_id, agent_one_score):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_one_score = %s
        WHERE id = %s
    """
    cursor.execute(query, (agent_one_score, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_two_score(game_id, agent_two_score):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_two_score = %s
        WHERE id = %s
    """
    cursor.execute(query, (agent_two_score, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_one_done(game_id):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_one_done = true
        WHERE id = %s
    """
    cursor.execute(query, (game_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_two_done(game_id):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_two_done = true
        WHERE id = %s
    """
    cursor.execute(query, (game_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_one_state(game_id, state):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_one_state = %s
        WHERE id = %s
    """
    cursor.execute(query, (state, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_agent_two_state(game_id, state):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        UPDATE barcade.games
        SET agent_two_state = %s
        WHERE id = %s
    """
    cursor.execute(query, (state, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_game_history(id):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = "SELECT * FROM barcade.game_history WHERE game_id=%s ORDER BY ts DESC"
    cursor.execute(query, (str(id),))
    results = cursor.fetchall()
    return results

def insert_game_history_event(game_id, action, agent_id, msg):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        INSERT INTO barcade.game_history (game_id, action, agent_id, ts, msg)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
    """
    cursor.execute(query, (str(game_id), action, str(agent_id), msg))
    conn.commit()
    cursor.close()
    conn.close()

def get_game_by_id(id):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = "SELECT * FROM barcade.games WHERE id=%s"
    cursor.execute(query, (str(id),))
    results = cursor.fetchall()
    return results

def get_active_games():
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = "SELECT * FROM barcade.games WHERE active=true"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def create_game(game_id, agent_one_id, agent_two_id, type, agent_one_state, agent_two_state):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()
    query = """
        INSERT INTO barcade.games (id, agent_one_id, agent_two_id, type, ts, active, agent_one_state, agent_two_state, agent_one_done, agent_two_done)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, TRUE, %s, %s, FALSE, FALSE)
        RETURNING id
    """
    cursor.execute(query, (str(game_id), str(agent_one_id), str(agent_two_id), type, agent_one_state, agent_two_state))
    game_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return game_id

def finish_game(game_id, winner):
    return ""