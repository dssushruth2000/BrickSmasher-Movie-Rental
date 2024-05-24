async function manageMovies(action, movieId, title = "") {
    const response = await fetch(manageMoviesURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ action, movie_id: movieId, title })
    });

    const result = await response.json();
    document.getElementById("message").innerText = result.message || result.error;

    
    if (!result.error) {
        refreshMovieTable();
    }
}


async function refreshMovieTable() {
    const response = await fetch('/movie/');
    const parser = new DOMParser();
    const doc = parser.parseFromString(await response.text(), 'text/html');

    
    const updatedTable = doc.querySelector('table').outerHTML;
    document.querySelector('table').outerHTML = updatedTable;
}


async function addNewMovie() {
    const title = document.getElementById("title").value;
    await manageMovies("new", null, title);
}
