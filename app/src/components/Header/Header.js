import './Header.css';
import { Link } from 'react-router-dom';
import GoogleBtn from '../GoogleBtn/GoogleBtn';
import AccessTokenContext from '../../context/AccessTokenContext';
import { useContext } from 'react';

const Header = () => {
  const { isLoggedIn } = useContext(AccessTokenContext);

  return (
    <div className="header">
      <div className="titleLogo">一緒に Sudoku</div>
      {isLoggedIn && (<Link to="/mypuzzles" className="nav-item">My Puzzles</Link>)}
      {isLoggedIn && (<Link to="/leaderboard-view" className="nav-item">Leaderboard</Link>)}
      <div className="login-btn" data-testid="login-btn">
        <GoogleBtn />
      </div>
    </div>
  );
};

export default Header;