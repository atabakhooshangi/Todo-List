const searchInput = document.getElementById('search-input')
const csrf = $('input[name=csrfmiddlewaretoken]').val()
const sendSearchQuery = (query) => {
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/search',
        data: {
            'csrfmiddlewaretoken': csrf,
            'query': query
        },
        data_type: 'html',
        success: (res) => {
            const data = res.data
            $('#tasklist').html(data)
        },
        error: (err) => {

        }

    });


}
searchInput.addEventListener('keyup', e => {
    sendSearchQuery(e.target.value)
})