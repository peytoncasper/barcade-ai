import React, { useState } from 'react';

const TowerOfHanoi = ({game}) => {
    return (
        <div className="grid place-items-center">

            <div className="towers">
                <div className="tower">
                    {game[0].map((disk) => (
                        <div key={disk} className="disk" style={{ width: `${disk * 30}px` }}></div>
                    ))}
                </div>
                <div className="tower">
                    {game[1].map((disk) => (
                        <div key={disk} className="disk" style={{ width: `${disk * 30}px` }}></div>
                    ))}
                </div>
                <div className="tower">
                    {game[2].map((disk) => (
                        <div key={disk} className="disk" style={{ width: `${disk * 30}px` }}></div>
                    ))}
                </div>
            </div>
            {/*<p>Moves: {moves}</p>*/}
            {/*{gameOver && <p>Congratulations! You solved the Tower of Hanoi puzzle in {moves} moves.</p>}*/}
            {/*<button onClick={resetGame}>Reset Game</button>*/}
        </div>
    );
};

export default TowerOfHanoi;