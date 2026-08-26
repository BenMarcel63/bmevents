console.log("Register JS connected");
const registerForm = document.getElementById("registerForm");


registerForm.addEventListener("submit", async(e)=>{


e.preventDefault();



const vendorData = {


businessName:
document.getElementById("businessName").value,


email:
document.getElementById("email").value,


phone:
document.getElementById("phone").value,


password:
document.getElementById("password").value


};



const response = await fetch(
"http://localhost:5000/register",
{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(vendorData)

}

);



const result = await response.json();



alert(result.message);


});