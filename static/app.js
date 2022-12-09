const BASE_API_URL = 'https://digimoncard.io/api-public/search.php?'

$('.nav-item').on('click','#search-button',()=>{
    generateSearchWindow();
})

$('#delete-button').on('click', (e) => {
    generateDeleteConfirmation();
})

$('#adv-search').on('submit', (e) => {
    e.preventDefault();
    $('option[value=""]').attr('disabled','')
    const params = $('#adv-search').serialize()
    getSearchResults(params)
})

$('#clear').on('click', (e) => {
    e.preventDefault();
    clearForm();
})

clearForm = () => {
    $('option[value=""]').removeAttr('disabled','')
    $('.list-cards').empty()
    $('input').val('')
    $('#adv-search').find('select').val('')
}

generateDeleteConfirmation = () => {
    createDeleteConfHTML();

    const dConf = $('#delete-conf')

    dConf.on('click', '.cancel', () => {
        dConf.remove()
    })
}

createDeleteConfHTML = () => {
    $('body').prepend($('<div>').attr('id','delete-conf').addClass('container-sm bg-light p-2'))

    let deleteTitle = $('<h3>').addClass('text-center').text('Are you sure you want to delete your profile?')

    let deleteConfImg = $('<img>').attr('src','/static/terriermon.png').addClass('img-fluid')

    let buttons = $('<div>').addClass('row justify-content-center')

    let dForm = $('<form>').attr('id','d-form').attr('action','http://127.0.0.1:5000//users/delete').attr('method','POST').addClass('col-4 p-0')

    let cancelBtn = $('<button>').addClass('btn btn-outline-primary col-4 m-1 cancel').text('Cancel')

    let confDeleteBtn = $('<button>').attr('type','submit').addClass('btn btn-danger form-control m-1').text('Confirm Delete')

    dForm.append(confDeleteBtn)

    buttons.append(cancelBtn,dForm)

    $('#delete-conf').append(deleteTitle,deleteConfImg,buttons)
}

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

    $('#search-window').on('click', 'img', (e) => {
        handleCardClick(e);
    })
}

createSearchHTML = () => {
    $('body').prepend($('<div>').attr('id','search-window').addClass('bg-light mt-2'));

    let closeBtn = $('<button>').addClass('btn btn-sm btn-basic ms-auto close').text('X')
    
    let searchTitle = $('<h2>').text('Search Digimon Cards')
    
    let sContent = $('<div>').attr('id','s-content').addClass('justify-content-center')

    let searchForm = '<form id="search_form"><input id="search" name="n" type="text" class="form-control mb-1" placeholder="Search cards by name"/><p class=" mb-1"><b>-or-</b></p></form>'
    
    let advBtn = $('<button>').addClass('btn btn-lg btn-primary mb-4').text('Advanced Search')
    
    let cardResults = $('<div>').addClass('list-cards')

    let searchHeader = $('<div>').addClass('d-flex m-1').append(searchTitle, closeBtn)

    $('#search-window').append(sContent)
    $('#s-content').append(searchHeader,searchForm,advBtn,cardResults)
}

async function getSearchResults(params) {
    const DCG = '&series=Digimon Card Game'
    const queryStr = `${params}${DCG}`

    $('.list-cards').empty();

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

$('.db-search-results').on('click','img', (e) => {
    handleDBCardClick(e);
})

handleCardClick = (e) => {
    const cardNum = $(e.target).closest('div').attr('data-card-num')

    window.location.href = '/cards/' + cardNum
}

handleDBCardClick = (e) => {
    const cardNum = $(e.target).closest('div').attr('data-card-num')
    
    DBHandler(cardNum)
}

DBHandler = (cardNum) => {
    const mDeck = []
    const eDeck = []
    const sDeck = []

    if ($('#card-sorter').val() === 'main') {
        mDeck.push(cardNum)
        const cardStats = [...getCardData(cardNum)]
        console.log(cardStats)
        
    }
}

async function getCardData(cardNum) {
    const mainDeck = $('.main-deck')
    const eggDeck = $('.egg-deck')
    const sideDeck = $('.side-deck')

    await axios.post(`/cards/${cardNum}`).then(resp => {
        console.log(resp)
    }).catch((err) => {
        console.log(err)
    })
}

class Deck {
    constructor(mainDeck,eggDeck,sideDeck) {
        this.mainDeck = mainDeck
        this.eggDeck = eggDeck
        this.sideDeck = sideDeck
    }
    mDeckLength() {
        return this.mainDeck.length === 50
    }
    eDeckLength() {
        return this.eggDeck.length <= 5
    }
    sDeckLength() {
        return this.sideDeck.length <= 10
    }
    checkInstancesOfCard() {

    }
}

