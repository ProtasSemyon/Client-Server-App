const loginName = document.querySelector('#login-name');

const jwt_token = localStorage.getItem('jwt_token');

fetch('/api/get_username/', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization' :'Bearer '+ jwt_token
  }
}
)
  .then(response => response.json())
  .then(data => {
    loginName.textContent = data.user_info.name
    console.log(data);
  })
  .catch(error => {
    console.error(error);
  });

