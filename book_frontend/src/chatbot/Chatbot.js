import React , {useEffect } from 'react';

import { Widget , addResponseMessage } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import logo from '../logo.svg';

import './chatbot_style.css';
import axios from 'axios';


export default function Chatbot() {
    useEffect(() => {
        addResponseMessage('Welcome to our page! Feel free to chat with me about book.');
    }, []);
    
    const handleChatbotUserMessageAxios = (newMessage) => {
        const headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin' : true,
            'Access-Control-Allow-Credentials': true
        }
        axios.post(
            `http://localhost:5000/api/dialogflow`,
            {user_input: newMessage}, {headers:headers}
        ).then(function(res) {
            addResponseMessage(res.data['response']);
        }).catch(function(error){console.log(error)})
    };
    
    const handleChatbotUserMessage = (newMessage) => {
        fetch('http://localhost:5000/api/dialogflow', {
            method: 'post', 
            mode: 'no-cors',
            headers: {
                'Access-Control-Allow-Origin': true,
                'Access-Control-Allow-Credentials': true,
                
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_input: newMessage})
        })
        .then(function(res) {
            res.json().then((r)=>{addResponseMessage(r['response'])})
            .catch(function(error){console.log(error)});
        }).catch(function(error){console.log(error)})
        
    };
    
    return (
        <Widget 
            handleNewUserMessage={handleChatbotUserMessageAxios}
            profileAvatar={logo}
            titleAvatar={logo}
            title="Book Chatbot"
            subtitle="please be patient..."
            showTimeStamp={false}
          />
    )
}