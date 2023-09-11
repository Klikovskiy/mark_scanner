let burger = document.querySelector(".burger");
burger.addEventListener("click", function(){
	burger.classList.toggle("active");
	document.querySelector(".menu").classList.toggle("active");
	document.querySelector(".wrapper").classList.toggle("active");

})