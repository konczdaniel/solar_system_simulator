// if error occured during Login

const loginButton = document.getElementById("login-conf-button");
if(loginButton.textContent === "Login!"){
    loginButton.textContent = "Bad Credentials!";
    loginButton.style.backgroundColor = "#ffdddd";
    loginButton.style.color = "red";
    loginButton.style.border = "1px solid transparent";
    
    setTimeout(() => {
        loginButton.textContent = "Login";
        loginButton.style.backgroundColor = "rgb(0, 94, 255)";
        loginButton.style.color = "white";
        loginButton.style.border = "1px solid transparent";
    }, 2500);
}

