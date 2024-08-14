document.getElementById('loginBtn').onclick = function() {
    document.getElementById('loginModal').style.display = 'flex';
}

document.getElementById('registerBtn').onclick = function() {
    document.getElementById('registerModal').style.display = 'flex';
}

document.getElementById('closeLogin').onclick = function() {
    document.getElementById('loginModal').style.display = 'none';
}

document.getElementById('closeRegister').onclick = function() {
    document.getElementById('registerModal').style.display = 'none';
}
