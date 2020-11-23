import React from "react";
import io from 'socket.io-client';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import HeartIcon from './heart.svg';

const client = new W3CWebSocket('ws://127.0.0.1:5000');

class Dashboard extends React.Component {
    state = {
        socketData: "",
        socketStatus:"On",
        heartRate: "Waiting...",
        pulse: 1
    }

    componentWillMount() {
        client.onopen = () => {
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            console.log(message);
            console.log(JSON.parse(message.data))
            this.setState({'heartRate': JSON.parse(message.data).message.heart_rate})

            this.setState({'pulse': 60 / this.state.heartRate })
        };
    }

    render() {
        const heartBeatStyle = {
            height: '2em',
            animation: 'heartbeat ' + this.state.pulse + 's infinite'
        }

        return (
            <React.Fragment>
            <div id="heartRate"><img src={HeartIcon} style={heartBeatStyle} alt="Heart" id="heart"/>{this.state.heartRate}</div>
            </React.Fragment>
        )
    }
}
export default Dashboard;