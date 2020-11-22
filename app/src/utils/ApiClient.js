const register = (accessToken) => {
    const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}` },
      };
      fetch('/register', requestOptions).then(res => res.json()).then(data => {
        console.log(data)
      });
}

export default register;