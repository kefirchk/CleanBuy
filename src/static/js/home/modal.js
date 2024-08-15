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

document.addEventListener('DOMContentLoaded', function() {
    var roleSelect = document.getElementById('role');
    var buyerInfoSection = document.getElementById('buyerInfo');

    roleSelect.addEventListener('change', function() {
        if (roleSelect.value === 'BUYER') {
            buyerInfoSection.style.display = 'block';
        } else {
            buyerInfoSection.style.display = 'none';
        }
    });

    // Инициализация состояния при загрузке страницы
    if (roleSelect.value === 'BUYER') {
        buyerInfoSection.style.display = 'block';
    } else {
        buyerInfoSection.style.display = 'none';
    }

    const addCountryButton = document.getElementById('addCountry');
    const countryList = document.getElementById('countryList');

    addCountryButton.addEventListener('click', function() {
        const newCountryInput = document.createElement('input');
        newCountryInput.type = 'text';
        newCountryInput.className = 'country-input';
        newCountryInput.placeholder = 'Country';

        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.className = 'country-button';
        removeButton.textContent = '-'; // Символ для кнопки удаления
        removeButton.addEventListener('click', function() {
            countryList.removeChild(removeButton.parentElement);
        });

        const newDiv = document.createElement('div');
        newDiv.className = 'form-group';
        newDiv.appendChild(newCountryInput);
        newDiv.appendChild(removeButton);

        countryList.appendChild(newDiv);
    });
});
