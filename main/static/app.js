const BASE_API_URL = 'https://digimoncard.io/api-public/search.php?'

$(document).ready(() => {
    if ($('#username')) {
        $('#username').focus()
    }
    if (window.location.href == '/cards/advanced') {
        $('#search-button').addClass('d-none')
    }
    if (window.location.href == '/decks') {
        if (!sessionStorage['tipsClosed']) {
            return showTips()
        }
    }
})

// on click events.

$('.nav-item').on('click','#search-button',()=>{
    $('input[name=n]').focus()
    $('.list-cards').empty()
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

$('.adv-search').on('submit', (e) => {
    e.preventDefault();
    $('option[value=""]').attr('disabled','')
    const params = $('.adv-search').serialize()
    getSearchResults(params)
})

$('.results').on('click', 'img', (e) => {
    handleCardClick(e);
})

$('.clear').on('click', (e) => {
    e.preventDefault();
    clearForm();
})

$('#messages').on('click', '.btn-close', () => {
    $('#messages').remove()
})

$('.toast-container').on('click', '.btn-close', () => {
    $('.toast').parent().remove()
})

$('#pre-DB-content').on('click', '#tips-close', () => {
    sessionStorage.setItem('tipsClosed', true)
    $('#tips').remove()
})

$('#deck-builder-btn').on('click', (e) => {
    e.preventDefault();
    $('#pre-DB-content').remove()
    $('#DB').removeClass('d-none')
    $('input[name="n"]').focus()
    $('.list-cards').empty();
    new Deck(50,5,10,4).startDB()
})

$('#adv-input').keydown((e) => {
    // if Enter key pressed in search input field.
    const keyCode = (e.keyCode ? e.keyCode : e.which)

    if (keyCode === 13) {
        e.preventDefault();
        $('#search-btn').click()
    }
})

// DOM manip and API calls

DBTipsHTML = () => {
    const preDBContent = $('#pre-DB-content')

    const tiplist1 = ['Main Deck must have 50 cards.','Egg and Side decks are optional.','You can only have 4 copies of any one card between your Main/Egg and Side decks.']

    const tiplist2 = ['12 - LVL 3 cards','10 - LVL 4 cards','8 - LVL 5 cards','4 - LVL 6 cards','4 - Tamers','12 - Options']

    const tipsRow = $('<div>').attr('id','tips').addClass('row mx-auto justify-content-center')
    const deckConstraints = $('<div>').addClass('col-10 col-md-4')
    
    preDBContent.append(tipsRow.append(deckConstraints))

    const list1HTML = $('<ul>').addClass('list-group list-group-flush')
    const list1Header = $('<li>').addClass('d-flex list-group-item text-center')
    const list1H2 = $('<h2>').addClass('mt-3').html('Deck builder tips.')
    const tipsCloseBtn = $('<button>').attr('id','tips-close').addClass('btn btn-basic btn-close ms-auto mt-3 pt-3')

    deckConstraints.append(list1HTML)
    list1HTML.append(list1Header.append(list1H2,tipsCloseBtn))

    for (let tip in tiplist1) {
        let tHTML = $('<li>').addClass('list-group-item text-center')
                             .append($('<span>').html(tiplist1[tip]))

        list1HTML.append(tHTML)
    }

    const listConnect = $('<li>').addClass('list-group-item text-center')
    const list2HTML = $('<ul>').addClass('list-group list-group-flush')

    list1HTML.append(listConnect)
    listConnect.append(list2HTML)

    const list2Header = $('<li>').addClass('list-group-item text-center')
    const list2H3 =  $('<h3>').addClass('mt-3').html('Recommended for a balanced deck.')

    list2HTML.append(list2Header.append(list2H3))

    const subListConnect = $('<li>').addClass('list-group-item text-center')
    const subListHTML = $('<ul>').addClass('tip-list2')

    list2HTML.append(subListConnect.append(subListHTML))

    for (let tip in tiplist2) {
        let tHTML = $('<li>').html(tiplist2[tip])

        subListHTML.append(tHTML)
    }
}

showTips = () => {
    const tipsHTML = DBTipsHTML()

    $('#pre-DB-content').append(tipsHTML)
}

clearForm = () => {
    $('input').val('')
    $('.list-cards').empty()
    $('.adv-search').find('select').val('')
    $('input[name=n]').focus()
}

doLoader = () => {
    const loader = $('<div>').addClass('text-center loading')

    const loadIMG = $('<img>').attr('src','/static/loading_gear_gif2.gif')

    loader.append(loadIMG)
    $('.list-cards').append(loader);
}

async function getSearchResults(params) {
    const DCG = '&series=Digimon Card Game'
    const queryStr = `${params}${DCG}`

    $('.list-cards').empty();

    doLoader()

    await axios
            .get(`${BASE_API_URL}` + queryStr)
            .then((res) => {
                handleSearch(res)
            })
            .catch((err) => {
                if (err.response.status === 400) {
                    const noResults = $('<h3>').addClass('text-center').html('~ No results found. ~')

                    $('.list-cards').append(noResults)
                }
            })
            .finally(() => {
                $('.loading').remove()
            });
}

getHoverStats = (card) => {    
    const stats = []

    for (let stat in card) {
        if (card[stat] !== null && stat !== 'image_url') {
            stats.push(`${stat}: ${card[stat]}`)
        }
    }
    const statsStr = stats.join('\r\n')
    return statsStr
}

createCardHTML = (card) => {
    const stats = getHoverStats(card)

    return `
    <div data-card-num=${card.cardnumber} class='search-card mb-4 col-5 col-md-3 col-lg-2' data-bs-toggle="tooltip" title="${stats}">
    <img class='card-img search-card-img' src='${card.image_url}' alt='${card.name}'/>
    </div>
    `
}

handleSearch = (res) => {
    let cards = res.data

    if (cards.length <= 5) {
        cards.forEach(card => {
            let newCard = $(createCardHTML(card)).attr('style','min-width: 270px')
            $('.list-cards').append(newCard);
        })
    } else {
        cards.forEach(card => {
            let newCard = $(createCardHTML(card))
            $('.list-cards').append(newCard);
        })

    }
}

handleCardClick = (e) => {
    const cardNum = $(e.target).closest('div').attr('data-card-num')

    window.location.href = '/cards/' + cardNum
}