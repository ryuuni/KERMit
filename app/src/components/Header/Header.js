import './Header.css';
import { Link } from 'react-router-dom';
import GoogleBtn from '../GoogleBtn/GoogleBtn';
import AccessTokenContext from '../../context/AccessTokenContext';
import { useContext } from 'react';

const Header = () => {
  const { isLoggedIn } = useContext(AccessTokenContext);

  return (
    <div className="header">
      <div className="title">一緒に Sudoku</div>
      {isLoggedIn && (
        <div className="nav-item">
          <Link to="/mypuzzles" style={{ textDecoration: 'none', color: 'rgb(43, 43, 43)'}}>My Puzzles</Link>
        </div>
      )}
      {isLoggedIn && (
        <div className="nav-item">
          <Link to="/leaderboard-view" style={{ textDecoration: 'none',  color: 'rgb(43, 43, 43)' }}>Leaderboard</Link>
        </div>
      )}
      <div className="login-btn" data-testid="login-btn">
        <GoogleBtn />
      </div>
    </div>
  );
};

export default Header;