import './App.css';
import Auth from './Auth'
import GoogleBtn from './GoogleBtn';
import Home from './Home';
import { Link, Route, Switch } from "react-router-dom";

function App() {
  const auth = new Auth();

  return (
    <div className="App" data-testid="app">
      <div data-testid="login-btn">
        <GoogleBtn auth={auth}/>
      </div>
      <Switch>
        <Route exact path="/"><Home auth={auth}/></Route>
        <Route path="/hello"><div>{'hello'}</div></Route>
      </Switch>
    </div>
  );
}

export default App;
