// Задаем параметры для OAuth 2.0
const googleClientId = '703772874802-hg25j5apmdseok1d205cnn7c9nemr7ph.apps.googleusercontent.com'; 
const googleRedirectUri = 'http://127.0.0.1:8000/api/google_auth/'; 
const googleScope = 'profile email'; 

const githubClientId = '87cd4f614d142bd3ad42'
const githubRedirectUri = 'http://127.0.0.1:8000/api/github_auth/'

const googleLoginButton = document.querySelector('#google');
const gitHubLoginButton = document.querySelector('#github');

const exitAccountButton = document.querySelector('#exit');


function googleRedirect() {
  const authUrl = `https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=${googleClientId}&redirect_uri=${googleRedirectUri}&scope=${googleScope}`;
  window.location.href = authUrl;
}

function githubRedirect() {
  const url = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${githubRedirectUri}`; 
  window.location.href = url;
}

googleLoginButton.addEventListener('click', () => {
  googleRedirect()
  fetch('/api/get_jwt_token/')
  .then(response => response.json())
  .then(data => {
    const token = data.jwt_token;
    localStorage.setItem('jwt_token', token);
  })
  .catch(error => {
    console.error(error);
  });
});

gitHubLoginButton.addEventListener('click', () => {
  githubRedirect()
  fetch('/api/get_jwt_token/')
  .then(response => response.json())
  .then(data => {
    const token = data.jwt_token;
    localStorage.setItem('jwt_token', token);
  })
  .catch(error => {
    console.error(error);
  });
})


exitAccountButton.addEventListener('click', () => {
  localStorage.removeItem('jwt_token');
  fetch('/')
})


