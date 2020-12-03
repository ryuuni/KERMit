import React, { useState, useContext} from 'react'
import PropTypes from 'prop-types';
import CurrentUserContext from '../../context/CurrentUserContext';
import './SudokuCell.css'

const backgroundColors = Object.freeze([
  'aliceblue',
  'honeydew',
  'lavender',
  'lavenderblush',
]);

export default function SudokuCell(props) {
  const {userEmail} = useContext(CurrentUserContext);
  console.log('USER EMAIL:');
  console.log(userEmail);
  const {player, index} = props.playerData ?? {};
  const [value, setValue] = useState(props.number);
  const style = {};
  if (props.x % 3 === 0) {
    style.borderLeft = '3px solid black';
  }
  if (props.y % 3 === 0) {
    style.borderTop = '3px solid black';
  }
  style.borderRight = (props.x % 3 === 2) ? '3px solid black' : 'none';
  style.borderBottom = (props.y % 3 === 2) ? '3px solid black' : 'none';

  style.backgroundColor = (index === undefined || index === -1) ? 'white' : backgroundColors[index];
  console.log(index);

  const firstName = player ? `${player.first_name.charAt(0).toUpperCase()}${player.first_name.slice(1)}` : '';
  const playerDisplayName = 
    player ? (player.last_name ? `${firstName} ${player.last_name[0].toUpperCase()}.` : firstName) : '';

  const className = props.prefilled ? 'fixedCell' : 'inputCell';
  return (
    <input 
      type="text"
      pattern="[1-9]"
      className={className}
      style={style}
      readOnly={props.prefilled || (props.playerData && props.playerData.player.email !== userEmail)}
      value={value || ''}
      onFocus={props.addLock}
      onBlur={props.removeLock}
      onInput={event => {
        const userInput = (event.target.validity.valid) ? 
          event.target.value : value;

        if (value !== userInput) {        
          setValue(userInput);
          props.onNumberChanged(userInput);
        }
      }}
      title={playerDisplayName}
    />
  );
};

SudokuCell.defaultProps = {
  number: null,
  prefilled: false,
  onNumberChanged: () => {},
  x: 0,
  y: 0,
  playerData: null,
};

SudokuCell.propTypes = {
  number: PropTypes.number,
  prefilled: PropTypes.bool.isRequired,
  onNumberChanged: PropTypes.func,
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
  playerData: PropTypes.shape({
    player: PropTypes.shape({
      id: PropTypes.number.isRequired,
      first_name: PropTypes.string.isRequired,
      last_name: PropTypes.string,
      email: PropTypes.string,
    }),
    index: PropTypes.number,
  }),
  addLock: PropTypes.func.isRequired,
  removeLock: PropTypes.func.isRequired,
};