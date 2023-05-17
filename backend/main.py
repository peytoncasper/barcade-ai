import datetime
import json
import logging
import time
import uuid

import flask
from langchain.llms import OpenAI
from flask import Flask, jsonify, request

import db
from db import get_active_games
import threading
from towers import TowersOfHanoiGame, TowersOfHanoiAgent
from tweet_battles import TweetBattleGame, TweetBattleAgent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG

@app.route('/init', methods=['GET'])
def init():
    active_games = db.get_active_games()

    resp = []

    for game in active_games:
        data = {
            "id": game[0],
            "type": game[6],
            "agent_one_state": json.loads(game[7]),
            "agent_two_state": json.loads(game[8]),
            "agent_one_done": game[9],
            "agent_two_done": game[10]
        }
        history = db.get_game_history(game[0])
        agent_one_turns = []
        agent_two_turns = []
        for event in history:
            if event[1] != "":
                if event[2] == game[1]:
                    if game[6] == "towers_of_hanoi":
                        agent_one_turns.append(event[1].split(" "))
                    else:
                        agent_one_turns.append(event[1])
                else:
                    if game[6] == "towers_of_hanoi":
                        agent_two_turns.append(event[1].split(" "))
                    else:
                        agent_two_turns.append(event[1])
        data["agent_one_turns"] = agent_one_turns
        data["agent_two_turns"] = agent_two_turns

        resp.append(data)
    return jsonify(resp)

class GameRunner():
    def __init__(self, game_id):
        self.agent_one_game = None
        self.agent_two_game = None
        self.agent_one = None
        self.agent_two = None
        self.game_id = game_id

    def run(self):
        game = db.get_game_by_id(self.game_id)[0]
        history = db.get_game_history(self.game_id)

        past_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=30)

        llm = OpenAI(temperature=0.9, openai_organization="org-VnhwCgUQPa24L6ZjQNQllWye")

        agent_one_history = []
        agent_two_history = []

        for event in history:
            if event[2] == game[1]:
                agent_one_history.append(event[4])
            elif event[2] == game[2]:
                agent_two_history.append(event[4])

        agent_one_done = game[9]
        if self.agent_one is None and agent_one_done is False:
            agent_one_state = json.loads(game[7])

            if game[6] == "towers_of_hanoi":
                self.agent_one_game = TowersOfHanoiGame(agent_one_state)
                # See if the game has been finished, but not updated
                if self.agent_one_game.won:
                    db.update_agent_one_done(self.game_id)
                # Else start an agent
                else:
                    self.agent_one = TowersOfHanoiAgent(model=llm, env=self.agent_one_game)
                    self.agent_one.ret = game[9]
                    self.agent_one.message_history = agent_one_history
            elif game[6] == "tweet_battle":
                self.agent_one_game = TweetBattleGame(agent_one_state)

                if self.agent_one_game.won:
                    db.update_agent_one_done(self.game_id)
                else:
                    self.agent_one = TweetBattleAgent(model=llm, env=self.agent_one_game, personality="Cyberpunk George Washington")
                    self.agent_one.ret = game[11]
                    self.agent_one.message_history = agent_one_history

        else:
            if game[6] == "towers_of_hanoi":
                self.agent_one_game = TowersOfHanoiGame([])
                self.agent_one_game.won = True
            elif game[6] == "tweet_battle":
                self.agent_one_game = TweetBattleGame(5)
                self.agent_one_game.won = True

        agent_two_done = game[10]
        if self.agent_two is None and agent_two_done is False:
            agent_two_state = json.loads(game[8])

            if game[6] == "towers_of_hanoi":
                self.agent_two_game = TowersOfHanoiGame(agent_two_state)

                # See if the game has been finished, but not updated
                if self.agent_two_game.won:
                    db.update_agent_two_done(self.game_id)
                # Else start an agent
                else:
                    self.agent_two = TowersOfHanoiAgent(model=llm, env=self.agent_two_game)
                    self.agent_two.ret = game[10]
                    self.agent_two.message_history = agent_two_history
            elif game[6] == "tweet_battle":
                self.agent_two_game = TweetBattleGame(agent_two_state)

                # See if the game has been finished, but not updated
                if self.agent_two_game.won:
                    db.update_agent_two_done(self.game_id)
                # Else start an agent
                else:
                    self.agent_two = TweetBattleAgent(model=llm, env=self.agent_two_game, personality="Spicy Galileo From the Stars")
                    self.agent_two.ret = game[12]
                    self.agent_two.message_history = agent_two_history

        else:
            if game[6] == "towers_of_hanoi":
                self.agent_two_game = TowersOfHanoiGame([])
                self.agent_two_game.won = True
            elif game[6] == "tweet_battle":
                self.agent_two_game = TweetBattleGame(5)
                self.agent_two_game.won = True


        while self.agent_one_game.won is False or self.agent_two_game.won is False:

            if game[6] == "towers_of_hanoi":
                if self.agent_one and len(self.agent_one.message_history) > 50:
                    db.update_agent_one_done(self.game_id)
                    self.agent_one_game.won = True
                elif self.agent_one_game.won is False:
                    src_tower, dest_tower = self.agent_one.act()

                    # Store action in DB
                    action = "{} {}".format(src_tower, dest_tower)
                    msg = "Action: " + action
                    db.insert_game_history_event(self.game_id, action, game[1], msg)

                    observation = self.agent_one_game.move_disk(src_tower, dest_tower)
                    obs_message = self.agent_one.observe(observation)
                    db.update_agent_one_state(self.game_id, self.agent_one_game.get_state())
                    # Store observation in DB
                    db.insert_game_history_event(self.game_id, "", game[1], obs_message)
                else:
                    self.agent_one_game.won = True
                    db.update_agent_one_done(self.game_id)

                if self.agent_two and len(self.agent_two.message_history) > 50:
                    db.update_agent_two_done(self.game_id)
                    self.agent_two_game.won = True
                if self.agent_two_game.won is False:
                    src_tower, dest_tower = self.agent_two.act()

                    # Store action in DB
                    action = "{} {}".format(src_tower, dest_tower)
                    msg = "Action: " + action
                    db.insert_game_history_event(self.game_id, action, game[2], msg)

                    observation = self.agent_two_game.move_disk(src_tower, dest_tower)
                    obs_message = self.agent_two.observe(observation)
                    db.update_agent_two_state(self.game_id, self.agent_two_game.get_state())
                    # Store observation in DB
                    db.insert_game_history_event(self.game_id, "", game[2], obs_message)

                else:
                    self.agent_two_game.won = True
                    db.update_agent_two_done(self.game_id)
                time.sleep(10)
            elif game[6] == "tweet_battle":
                if self.agent_one and len(self.agent_one.message_history) > 12:
                    db.update_agent_one_done(self.game_id)
                    self.agent_one_game.won = True
                elif self.agent_one_game.won is False:
                    tweet = self.agent_one.act()

                    # Store action in DB
                    msg = "Tweet: " + tweet
                    db.insert_game_history_event(self.game_id, tweet, game[1], msg)

                    self.agent_one_game.add_tweet(self.agent_two_game.last_tweet)
                    obs_message = self.agent_one.observe(self.agent_two_game.last_tweet, 0)
                    db.update_agent_one_state(self.game_id, self.agent_one_game.get_state())
                    # Store observation in DB
                    db.insert_game_history_event(self.game_id, "", game[1], obs_message)
                else:
                    self.agent_one_game.won = True
                    db.update_agent_one_done(self.game_id)

                # Agent 2 Turn
                if self.agent_two and len(self.agent_two.message_history) > 12:
                    db.update_agent_two_done(self.game_id)
                    self.agent_two_game.won = True
                if self.agent_two_game.won is False:
                    tweet = self.agent_two.act()

                    # Store action in DB
                    msg = "Tweet: " + tweet
                    db.insert_game_history_event(self.game_id, tweet, game[2], msg)

                    self.agent_two_game.add_tweet(self.agent_one_game.last_tweet)
                    obs_message = self.agent_two.observe(self.agent_one_game.last_tweet, 0)
                    db.update_agent_one_state(self.game_id, self.agent_one_game.get_state())
                    # Store observation in DB
                    db.insert_game_history_event(self.game_id, "", game[2], obs_message)

                else:
                    self.agent_two_game.won = True
                    db.update_agent_two_done(self.game_id)
                time.sleep(1)
        db.deactivate_game(game[0])
        return ""
class Matchmaker():
    def __init__(self):
        self.playable_games = ["towers_of_hanoi", "tweet_battle"]

    def run(self):
        while True:
            games = get_active_games()

            for t in self.playable_games:
                hasGame = False
                for g in games:
                    if g[6] == t:
                        hasGame = True
                if not hasGame:
                    self.add_game(t)

                games = get_active_games()


            for game in games:
                game_id = game[0]
                # Handle no active runner
                runner = GameRunner(game[0])
                t = threading.Thread(daemon=True, target=runner.run)
                t.start()
                print("Starting runner")

            time.sleep(30)

    def add_game(self, type):
        game_id = uuid.uuid4()
        agent_one_id = uuid.uuid4()
        agent_two_id = uuid.uuid4()
        if type == "towers_of_hanoi":
            db.create_game(game_id, agent_one_id, agent_two_id, type, str([[1,2,3],[],[]]), str([[1,2,3],[],[]]))

            action = TowersOfHanoiAgent(None, None).instructions
            db.insert_game_history_event(game_id, "",agent_one_id, action)
            db.insert_game_history_event(game_id, "",agent_two_id, action)
        elif type == "tweet_battle":
            db.create_game(game_id, agent_one_id, agent_two_id, type, 0, 0)

            action = TweetBattleAgent(None, None, None).instructions
            db.insert_game_history_event(game_id, "",agent_one_id, action)
            db.insert_game_history_event(game_id, "",agent_two_id, action)




if __name__ == '__main__':
    mm = Matchmaker()
    matchmaker = threading.Thread(target=mm.run)
    matchmaker.start()

    app.run(host='0.0.0.0', port=5001, debug=False)

    # llm = OpenAI(temperature=0.9)
    #
    # game = TowersOfHanoiGame()
    # agent = TowersOfHanoiAgent(llm, game)
    #
    # observation = game.reset()
    # agent.reset()
    #
    # obs_message = agent.observe(observation)
    # print(obs_message)
    #
    # while game.won is False:

        #
        # if termination or truncation:
        #     print('break', termination, truncation)
        #     break
    # env.close()
    #
    #
    # text = "What would be a good company name for a company that makes colorful socks?"
    #
    # prompt = PromptTemplate(
    #     input_variables=["product"],
    #     template="What is a good name for a company that makes {product}?",
    # )
    #
    # chain = LLMChain(llm=llm, prompt=prompt)
    #
    # print(chain.run("colorful socks"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
