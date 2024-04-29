const menu = document.getElementById('nav-dialog');
function handleMenu(){
    menu.classList.toggle("hidden");
}

const profile = document.getElementById("profile");
function handleProfile(){
    profile.classList.toggle("hidden");
}

function smoothScrollTo(targetId){
    const scrollToSearch = document.getElementById(targetId);
    if(scrollToSearch){
        window.scrollTo({
            top:scrollToSearch.offsetTop, 
            behavior: 'smooth'
        });
    }
}