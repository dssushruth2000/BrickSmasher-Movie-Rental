function displayError(message) {
    const errorDivs = document.querySelectorAll('.error-message');

    errorDivs.forEach(div => {
        div.textContent = message;
        div.style.color = 'red'; 
    });
}


async function submitRental(action, userId, movieId) {
    const response = await fetch(manageRentalsURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action, user_id: userId, movie_id: movieId })
    });

    const result = await response.json();

    
    const errorMessageElements = document.querySelectorAll('.error-message');

    if (result.error) {
       
        errorMessageElements.forEach(element => {
            element.innerText = result.error;
        });
    } else {
        
        errorMessageElements.forEach(element => {
            element.innerText = '';
        });

       
        findMember(); 
    }
}


function populateCheckedOutTable(rentals) {
    const checkedOutTableBody = document.querySelector('#checked-out-table tbody');
    checkedOutTableBody.innerHTML = ''; 
    rentals.forEach((rental, index) => {
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${rental.title}</td>
                <td><button onclick="submitRental('return', ${rental.user_id}, ${rental.movie_id})">Return</button></td>
            </tr>
        `;
        checkedOutTableBody.innerHTML += row;
    });
}

function populateMoviesTable(movies, userId) {
    const moviesTableBody = document.querySelector('#all-movies-table tbody');
    moviesTableBody.innerHTML = ''; 
    movies.forEach((movie, index) => {
        const actionButton = `<button onclick="submitRental('rent', ${userId}, ${movie.id})">Rent</button>`;
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${movie.title}</td>
                <td>${movie.in_stock}</td>
                <td>${actionButton}</td>
            </tr>
        `;
        moviesTableBody.innerHTML += row;
    });
}

async function findMember() {
    const email = document.getElementById('email').value;

    if (!email) {
        document.getElementById('member-info').innerHTML = '';
        document.querySelector('#checked-out-table tbody').innerHTML = '<tr><td colspan="3">Please provide a member email to see checked-out movies.</td></tr>';
        return;
    }

    const response = await fetch(`/rent/?email=${encodeURIComponent(email)}`);
    const result = await response.json();

    document.getElementById('member-info').innerHTML = result.member_info || 'No member information found';
    if (result.rentals_list) {
        populateCheckedOutTable(result.rentals_list);
    }
    if (result.all_movies_list) {
        populateMoviesTable(result.all_movies_list, result.user_id);
    }
}
