const BASE_API_URL = 'https://digimoncard.io/api-public/search.php?'

$('.nav-item').on('click','#search-button',(e)=>{
    generateSearchWindow();
})

generateSearchWindow = () => {
    
    createSearchHTML();    

    $('#search-window').on('click','.close', () => {
        $('#search-window').remove()
    })

    $('#search-window').on('submit','#search_form', (e) => {
        e.preventDefault();
        $('.list-cards').empty();
        let params =`n=${$('#search').val()}`;
        $('#search').val('');
        getSearchResults(params);
    })

    $('.list-cards').on('click', 'img', async function(e) {
        handleCardClick(e);
    })
}

createSearchHTML = () => {
    $('body').prepend($('<div>').attr('id','search-window').addClass('conatiner bg-light mt-2'));

    let closeBtn = $('<button>').addClass('btn btn-sm btn-basic ms-auto close').text('X')
    
    let searchTitle = $('<h2>').text('Search Digimon Cards')
    
    let sContent = $('<div>').attr('id','s-content').addClass('justify-content-center')

    let searchForm = '<form id="search_form"><input id="search" name="n" type="text" class="form-control mb-1" placeholder="Search cards by name"/><p class=" mb-1"><b>-or-</b></p></form>'
    
    let advBtn = $('<button>').addClass('btn btn-lg btn-primary mb-4').text('Advanced Search')
    
    let cardResults = $('<div>').addClass('list-cards card-columns')

    let searchHeader = $('<div>').addClass('d-flex m-1').append(searchTitle, closeBtn)

    $('#search-window').append(sContent)
    $('#s-content').append(searchHeader,searchForm,advBtn,cardResults)
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
        <div data-card-num=${card.cardnumber} class='search-card'>
        <img class='card-img search-card-img' src='${card.image_url}' alt='${card.name}'
        </div>
    `;
}

handleSearch = (res) => {
    let cards = res.data

    cards.forEach(card => {
        let newCard = $(createCardHTML(card))
        $('.list-cards').append(newCard);
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
