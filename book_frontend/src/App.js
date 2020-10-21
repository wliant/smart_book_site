import React , {useEffect } from 'react';
import './App.css';
import Blog from './blog/Blog';
import { Widget , addResponseMessage } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import logo from './logo.svg';

import './chatbot_style.css';

function App() {
    useEffect(() => {
        addResponseMessage('Welcome to our page! Feel free to chat with me about book.');
    }, []);
    
    const handleNewUserMessage = (newMessage) => {
        var replied = `your message is: ${newMessage}`
        // TODO: need to send to backend
        addResponseMessage(replied);
    };
  return (
    <div className="App">
      <Blog />
      <Widget 
        handleNewUserMessage={handleNewUserMessage}
        profileAvatar={logo}
        titleAvatar={logo}
        title="Book Chatbot"
        subtitle="please be patient..."
        showTimeStamp={false}
      />
    </div>
  );
}

export default App;
