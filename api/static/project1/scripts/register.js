// if error occured during registration
const createButton = document.getElementById("create-conf-button");
if(createButton.textContent === "Create configuration!"){
        createButton.textContent = "Username already exists!";
        createButton.style.backgroundColor = "#ffdddd";
        createButton.style.color = "red";
        createButton.style.border = "1px solid transparent";
    
    setTimeout(() => {
        createButton.textContent = "Create configuration";
        createButton.style.backgroundColor = "rgb(0, 94, 255)";
        createButton.style.color = "white";
        createButton.style.border = "1px solid transparent";
    }, 2500);
}