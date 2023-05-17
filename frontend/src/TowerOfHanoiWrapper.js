import TurnList from "./TurnList";
import TowerOfHanoi from "./TowersOfHanoi";
import {useEffect, useState} from "react";

const TowerOfHanoiWrapper = () => {
    let [state, setState] = useState({
        "type": "towers_of_hanoi",
        "agent_one_state": [[1,2,3],[],[]],
        "agent_two_state": [[1,2,3],[],[]],
        "agent_one_done": false,
        "agent_two_done": false,
        "agent_one_turns": [],
        "agent_two_turns": []
    });

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetch('http://127.0.0.1:5001/init').then(data => data.json()).then((json) => {
                if(json.length > 0 && json[0]["type"] === "towers_of_hanoi") {
                    setState(json[0])
                } else if (json.length > 1 && json[0]["type"] === "towers_of_hanoi") {
                    setState(json[1])
                } else {
                    setState({
                        "type": "towers_of_hanoi",
                        "agent_one_state": [[1,2,3],[],[]],
                        "agent_two_state": [[1,2,3],[],[]],
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
        <div className="flex flex-row gap-y-5 px-6 pb-4" style={{maxHeight: "90vh"}}>

            <div className="flex" style={{height: "75vh", overflow: "scroll"}}>
                <TurnList turns={state.agent_one_turns} agent={1}/>
            </div>
            <div className="flex" style={{height: "75vh", overflow: "scroll"}}>
                <TowerOfHanoi game={state.agent_one_state}/>
            </div>
            <div className="flex" style={{height: "75vh", overflow: "scroll"}}>
                <TowerOfHanoi game={state.agent_two_state}/>
            </div>
            <div className="flex  overflow-y-auto" style={{height: "75vh"}}>
                <TurnList turns={state.agent_two_turns} agent={2}/>
            </div>
        </div>
    )
}

export default TowerOfHanoiWrapper;
