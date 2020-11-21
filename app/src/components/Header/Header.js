import './Header.css';
import {Link} from 'react-router-dom';
import GoogleBtn from '../../GoogleBtn';
import AccessTokenContext from '../../context/AccessTokenContext';
import {useContext} from 'react';

const Header = () => {
  const {isLoggedIn, setAccessToken} = useContext(AccessTokenContext);

  return (
    <div className="header">
      <div className="title">一緒に Sudoku</div>
      {isLoggedIn && (
        <div className="nav-item">
          <Link to="/mypuzzles">My Puzzles</Link>
        </div>
      )}
      {isLoggedIn && (
        <div className="nav-item">
          <Link to="/leaderboard-view">Leaderboard</Link>
        </div>
      )}
      <div className="login-btn" data-testid="login-btn">
        <GoogleBtn onAccessTokenChanged={setAccessToken}/>
      </div>
    </div>
  );
};

export default Header;