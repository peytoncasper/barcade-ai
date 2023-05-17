import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";
import reportWebVitals from './reportWebVitals';
import TowerOfHanoiWrapper from "./TowerOfHanoiWrapper";
import TweetBattleWrapper from "./TweetBattleWrapper";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        children: [
            {
                path: "/",
                element: <TowerOfHanoiWrapper/>
            },
            {
                path: "/towers_of_hanoi",
                element: <TowerOfHanoiWrapper/>
            },
            {
                path: "/tweet_battles",
                element: <TweetBattleWrapper />,
            },
        ],
    },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
