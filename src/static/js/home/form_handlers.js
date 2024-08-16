async function sendDataForLogin(formData) {
    const login_response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString()
    });

    if (login_response.ok) {
        const data = await login_response.json();
        document.cookie = `Authorization=${data['access_token']}; path=/; secure; samesite=lax;`;
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
    let buyer_information = null //document.getElementById('buyerInfo').value
    if (role === 'BUYER') {
        const paymentOptions = Array.from(document.querySelectorAll('input[name="paymentOptions"]:checked'))
            .map(checkbox => checkbox.value);

        const importCountries = Array.from(document.querySelectorAll('.country-input'))
            .map(input => input.value.trim())
            .filter(value => value.length > 0); // Фильтруем пустые строки

        buyer_information = {
            location: {
                country: document.getElementById('country').value,
                city: document.getElementById('city').value
            },
            import_countries: importCountries,
            product_segment: document.getElementById('productSegment').value,
            commission_rate: {
                min_rate: parseInt(document.getElementById('minRate').value, 10),
                max_rate: parseInt(document.getElementById('maxRate').value, 10)
            },
            price_range: {
                min_price: parseInt(document.getElementById('minPrice').value, 10),
                max_price: parseInt(document.getElementById('maxPrice').value, 10)
            },
            delivery_options: document.getElementById('deliveryOptions').value,
            payment_options: paymentOptions,
            prepayment_percentage: parseInt(document.getElementById('prepaymentPercentage').value, 10)
        };
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
