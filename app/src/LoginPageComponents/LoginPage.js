import React, { Component } from 'react';
import GoogleBtn from './GoogleBtn';
import { Redirect } from "react-router-dom";

export default function LoginPage(props) {
  return (
    <div>
      <h1>Isshoni Sudoku</h1>
      <div className="login-btn" data-testid="login-btn">
        <GoogleBtn onAccessTokenChanged={accessToken => this.setState({accessToken})}/>
      </div>
    </div>

  );
}