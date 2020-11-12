import './App.css';
import GoogleBtn from './GoogleBtn';

function App() {
  return (
    <div className="App" data-testid="app">
      <div data-testid="login-btn">
        <GoogleBtn />
      </div>
    </div>
  );
}

export default App;
