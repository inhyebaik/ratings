"use strict";

function handleGenre(evt) {

    evt.preventDefault();
    let formInput = {
        "inputGenre": $("#genre-option").val()
    }

    $.get('/movie-filter.json', formInput, filterGenre);
}

function filterGenre(results) {

    $("#movie-list").empty();
    for (let movie in results) {
        $("#movie-list").append(
                  `<li>
                      <a href="/movies/${results[movie]}">
                        ${movie} (${results[movie]})
                      </a>
                  </li>`
            );
        }
}

$('#genre-option').on('change', handleGenre);
