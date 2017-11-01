"use strict";

function handleGenre(evt) {
    evt.preventDefault();
    console.log('test 2');

    let formInput = {
        "inputGenre": $("#genre-option").val()
    }

    $.get('/movie-filter.json', formInput, filterGenre);
}

function filterGenre(results) {
    console.log('test 3');
    $("#movie-list").empty();

    for (let movie in results){
        $("#movie-list").append(
                  `<li>
                      <a href="/movies/${movie.movie_id}">
                        ${movie.title} (${movie.movie_id})
                      </a>
                  </li>`
            );
        }
}

$('#genre-option').on('change', handleGenre);
