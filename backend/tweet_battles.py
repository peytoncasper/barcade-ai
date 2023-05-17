from langchain.output_parsers import RegexParser

class TweetBattleAgent:
    def __init__(self, model, env, personality):
        self.model = model
        self.env = env
        self.personality = personality
        self.instructions = """
Your goal is to write the spiciest tweets possible in response to your competitor. You'll receive your competitors
last tweet as an observation. Remember, you've been assigned a personality, stay in character. You'll also receive the
current number of likes you've received from the audience. The better your tweets, the more likes you get. Your goal
is to maximize the number of likes you get. User proper punctuation and spacing and don't include any special tokens such as <personality>, <observation> or <turns> or <likes>

Personality: <personality>
Observation: <observation>
Likes: <turns>

You will respond with a Tweet, formatted as below

Tweet: Yo! This is one spicy tweet. How many characters I got? 140? Thats it? 
        """

        self.action_parser = RegexParser(
            regex=r"Tweet: (.*)(\d+)$",
            output_keys=['tweet'],
            default_output_key='tweet')
        self.message_history = []
        self.ret = 0

    def reset(self):
        self.message_history = [
            # self.docs,
            self.instructions,
        ]

    def observe(self, obs, likes):

        obs_message = f"""
Personality: {self.personality}
Observation: {obs}
Likes: {self.ret}
        """
        self.message_history.append(obs_message)
        return obs_message
    def _act(self):
        tweet = ""
        validTweet = False

        while not validTweet:
            act_message = self.model(self.message_history)

            try:
                tweet = self.action_parser.parse(act_message)['tweet']
                self.message_history.append(act_message)
            except:
                self.message_history.append("The action is invalid because you did not match the syntax expected of Tweet: <tweet>")
            validTweet = True

        return tweet

    def act(self):
        tweet = self._act()
        return tweet

class TweetBattleGame:
    won = False

    def __init__(self, init_state):
        if init_state:
            self.current_state = init_state
        else:
            self.current_state = 0

        if self.current_state == 5:
            self.won = True

        self.last_tweet = ""

    def get_state(self):
        return str(self.current_state)

    def add_tweet(self, last_tweet):
        self.last_tweet = last_tweet
        self.current_state += 1
