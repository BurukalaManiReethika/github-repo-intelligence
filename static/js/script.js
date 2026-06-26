document.addEventListener("DOMContentLoaded",()=>{

const ctx=document.getElementById("languageChart");

if(ctx){

new Chart(ctx,{

type:"pie",

data:{

labels:[
"Python",
"HTML",
"CSS",
"JavaScript"
],

datasets:[{

data:[45,25,15,15]

}]

}

});

}

});
