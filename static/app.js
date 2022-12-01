const BASE_API_URL = 'https://digimoncard.io/api-public/search.php?'

$('.nav-item').on('click','#search-button',(e)=>{
    $('.search-window').remove();
    generateSearchWindow();
})

generateSearchWindow = () => {
    
    createSearchHTML();    

    $('.search-window').on('click','.close', () => {
        $('.search-window').remove()
    })

    $('.search-window').on('submit','#search_form', (e) => {
        e.preventDefault();
        $('#list-cards').empty();
        let params =`n=${$('#search').val()}`;
        $('#search').val('');
        getSearchResults(params);
    })
}

createSearchHTML = () => {
    $('body').append($('<div>').addClass('search-window'));

    let closeBtn = $('<button>').addClass('btn btn-sm btn-default close').text('X')
    
    let searchTitle = $('<h2>').text('Search Digimon Cards')
    
    let searchForm = '<form id="search_form"><input id="search" name="n" class="form-control mb-1" placeholder="Search cards by name"/><p class=" mb-1"><b>-or-</b></p></form>'
    
    let advBtn = $('<button>').addClass('btn btn-lg btn-primary mb-4').text('Advanced Search')
    
    let cardResults = $('<div>').attr('id','list-cards').addClass('card-group')

    let searchHeader = $('<section>').addClass('d-flex').append(searchTitle, closeBtn)

    let hr = $('<hr>')

    $('.search-window').append(searchHeader,hr,searchForm,advBtn,cardResults)
}

async function getSearchResults(params) {
    const DCG = '&series=Digimon Card Game'
    const queryStr = `${params}${DCG}`

    await axios
            .get(`${BASE_API_URL}` + queryStr)
            .then((res) => {
                handleSearch(res)
            })
            .catch((err) => {
                console.log(err)

            });
}

createCardHTML = (card) => {
    return `
        <div data-card-num=${card.cardnumber} class='card mb-3'>
        <img class='card-img' src='${card.image_url}' alt='${card.name}'
        </div>
    `;
}

handleSearch = (res) => {
    let cards = res.data

    $('#list-cards').on('click', 'img', async function(e) {
        handleCardClick(e);
    })

    cards.forEach(card => {
        let newCard = $(createCardHTML(card))
        $('#list-cards').append(newCard);
    })
}

handleCardClick = (e) => {
    let cardNum = $(e.target).closest('div').attr('data-card-num')
    try {
        window.location.href = '/cards/' + cardNum
    }
    catch (err) {
        console.log(err)
    }
}
