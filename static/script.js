async function sendMessage(){

let message = document.getElementById("message").value;

let chat = document.getElementById("chat");

chat.innerHTML += `
<div class="message user">
<span>${message}</span>
</div>
`;

let loading = `
<div class="message bot" id="loading">
<span>Typing...</span>
</div>
`;

chat.innerHTML += loading;

let response = await fetch("/api/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
message:message
})

});

let data = await response.json();

document.getElementById("loading").remove();

chat.innerHTML += `
<div class="message bot">
<span>${data.reply}</span>
</div>
`;

chat.scrollTop = chat.scrollHeight;

document.getElementById("message").value="";

}