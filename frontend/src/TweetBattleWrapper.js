import TurnList from "./TurnList";
import TowerOfHanoi from "./TowersOfHanoi";
import React, {useEffect, useState} from "react";
import TweetList from "./TweetList";

const TweetBattleWrapper = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

    const [state, setState] = useState({
        "type": "tweet_battle",
        "agent_one_state": 0,
        "agent_two_state": 0,
        "agent_one_done": false,
        "agent_two_done": false,
        "agent_one_turns": [],
        "agent_two_turns": []
    });

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetch(backendUrl + '/init').then(data => data.json()).then((json) => {
                if (json.length > 0 && json[0]["type"] === "tweet_battle") {
                    setState(json[0])
                } else if (json.length > 1 && json[1]["type"] === "tweet_battle") {
                    setState(json[1])
                } else {
                    setState({
                        "type": "tweet_battle",
                        "agent_one_state": 0,
                        "agent_two_state": 0,
                        "agent_one_done": false,
                        "agent_two_done": false,
                        "agent_one_turns": [],
                        "agent_two_turns": []
                    })
                }
            })
        }, 2000);

        return () => {
            clearInterval(intervalId);
        };
    }, []);
    return (
        <div className="flex flex-row gap-y-5 px-6 pb-4" style={{maxHeight: "90vh", width: "100%", maxWidth: "100%"}}>

            <div className="flex grow" style={{height: "75vh", overflow: "scroll", width: "50%"}}>
                <TweetList turns={state.agent_one_turns} agent={"Cyberpunk Washington"}/>
            </div>

            <div className="flex grow" style={{height: "75vh", overflow: "scroll", width: "50%"}}>
                <TweetList turns={state.agent_two_turns} agent={"Spicy Galileo From the Stars"}/>
            </div>
            {/*<div className="flex" style={{height: "75vh", overflow: "scroll"}}>*/}
            {/*    {state.length > 0 ? <TurnList turns={state[0].agent_one_turns} agent={1}/> : <div />}*/}
            {/*</div>*/}
            {/*<div className="flex" style={{height: "75vh", overflow: "scroll"}}>*/}
            {/*    {state.length > 0 ? <TowerOfHanoi game={state[0].agent_one_state}/> : null }*/}
            {/*</div>*/}
            {/*<div className="flex" style={{height: "75vh", overflow: "scroll"}}>*/}
            {/*    {state.length > 0 ? <TowerOfHanoi game={state[0].agent_two_state}/> : null }*/}
            {/*</div>*/}
            {/*<div className="flex  overflow-y-auto" style={{height: "75vh"}}>*/}
            {/*    {state.length > 0 ? <TurnList turns={state[0].agent_two_turns} agent={2}/> : <div />}*/}
            {/*</div>*/}
        </div>
    )
}

export default TweetBattleWrapper;
