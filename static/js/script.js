const form = document.querySelector("form");

if(form){

form.addEventListener("submit",()=>{

const button=document.querySelector("button");

button.innerHTML="Analyzing...";

button.disabled=true;

});

}
