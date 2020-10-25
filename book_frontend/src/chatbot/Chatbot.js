import React , {useEffect } from 'react';

import { Widget , addResponseMessage } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import logo from '../logo.svg';

import './chatbot_style.css';


export default function Chatbot() {
    useEffect(() => {
        addResponseMessage('Welcome to our page! Feel free to chat with me about book.');
    }, []);
    
    const handleChatbotUserMessage = (newMessage) => {
        fetch('/api/world', {
            method: 'post', 
            headers: {
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
            handleNewUserMessage={handleChatbotUserMessage}
            profileAvatar={logo}
            titleAvatar={logo}
            title="Book Chatbot"
            subtitle="please be patient..."
            showTimeStamp={false}
          />
    )
}