const register = (accessToken) => {
    const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}` },
      };
      fetch('http://localhost:5000/register', requestOptions).then(res => res.json()).then(data => {
        console.log(data)
      });
}

export default register;