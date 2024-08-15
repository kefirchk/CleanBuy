async function sendDataForLogin(formData) {
    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString()
    });

    if (response.ok) {
        alert('Login successful!');
        document.getElementById('loginModal').style.display = 'none';
        window.location.href = '/pages/chat';
    } else {
        alert('Login failed! Please check your credentials.');
    }
}

document.getElementById('loginForm').onsubmit = async function(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    await sendDataForLogin(formData)
}

document.getElementById('registerForm').onsubmit = async function(e) {
    e.preventDefault();

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const role = document.getElementById('role').value
    let buyer_information = document.getElementById('buyerInfo').value
    if (role === 'USER') {
        buyer_information = null
    }

    const response = await fetch('/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, role, buyer_information})
    });

    if (response.ok) {
        alert('Registration successful!');
        document.getElementById('registerModal').style.display = 'none';

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        await sendDataForLogin(formData)
    } else {
        alert('Registration failed! Please try again.');
    }
}
