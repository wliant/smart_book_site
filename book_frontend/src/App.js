import React , { useEffect } from 'react';
import './App.css';
import Blog from './blog/Blog';
import 'react-chat-widget/lib/styles.css';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import { BrowserRouter as Router, Switch } from 'react-router-dom';
import UnauthedRoute from "./UnauthedRoute";
import AuthedRoute from "./AuthedRoute";

function App() {

  return (
      <Router>
          <Switch>
              <UnauthedRoute path="/auth/login" component={SignIn} />
              <UnauthedRoute path="/auth/signUp" component={SignUp} />
              <AuthedRoute path="/" component={Blog} />
          </Switch>
      </Router>
  );
}

export default App;
