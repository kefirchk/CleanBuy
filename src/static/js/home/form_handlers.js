document.getElementById('loginForm').onsubmit = async function(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        alert('Login successful!');
        document.getElementById('loginModal').style.display = 'none';
        window.location.href = '/dashboard';
    } else {
        alert('Login failed! Please check your credentials.');
    }
}

document.getElementById('registerForm').onsubmit = async function(e) {
    e.preventDefault();

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    const response = await fetch('/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password })
    });

    if (response.ok) {
        alert('Registration successful!');
        document.getElementById('registerModal').style.display = 'none';
        window.location.href = '/login';
    } else {
        alert('Registration failed! Please try again.');
    }
}
