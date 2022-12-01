const BASE_API_URL = 'https://digimoncard.io/api-public/search.php?'

$('#search_form').on('submit',(e)=>{
    e.preventDefault();
    $('#list-cards').empty()
    let params =`n=${$('#search').val()}`;
    $('#search').val('')
    getSearchResults(params);
})

$('#list-cards').on('click', 'div', async function(e) {
    e.preventDefault();
    console.log(e.target)
    let card = $(e.target).closest('div')
    let cardID = card.attr('data-card-id')

    await axios.get(`http://127.0.0.1:5000/cards/${cardID}`)
})

async function getSearchResults(params) {
    const DCG = '&series=Digimon Card Game'
    const queryStr = `${BASE_API_URL}${params}${DCG}`

    await axios
            .get(queryStr)
            .then((res) => {
                generateSearchWindow()
                handleSearch(res)
            }).catch((err) => {
                console.log(err)

            });
}

createCardHTML = (card) => {
    return `
        <div data-card-id=${card.cardnumber} class='card mb-3'>
        <img class='card-img' src='${card.image_url}' alt='${card.name}'
        </div>
    `;
}

handleSearch = (res) => {
    $('.search-window').append($('<div id="list-cards" class="card-group"></div>'))

    let cards = res.data              

    cards.forEach(card => {
        console.log(card)
        let newCard = $(createCardHTML(card))
        $('#list-cards').append(newCard);
    })
}

generateSearchWindow = () => {
    $('body').append($('<div class="search-window"></div>'))
    $('.search-window').append('<button class="btn btn-lg btn-primary>Advanced Search</button>')
    $('.search-window').append('<button class="btn btn-sm close">X</button>')
}