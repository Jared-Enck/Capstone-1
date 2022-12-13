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
    // add hover stats here maybe? ***
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
    const cardNum = $(e.target).closest('div').attr('data-card-num')

    window.location.href = '/cards/' + cardNum
}

$('#deck-builder-btn').on('click', (e) => {
    e.preventDefault();
    $('#pre-DB-content').remove()
    $('#DB').removeClass('d-none')
    new Deck(50,5,10,4).startDB()
})

class Deck {
    constructor(mainLimit,eggLimit,sideLimit,cardLimit) {
        this.mainLimit = mainLimit
        this.eggLimit = eggLimit
        this.sideLimit = sideLimit
        this.cardLimit = cardLimit
        this.decklist = {
            mainDeck: [],
            eggDeck: [],
            sideDeck: []
        }
    }
    startDB = () => {    
        this.handleDBCardClick = this.handleClick.bind(this)
        $('.db-search-results').on('click','img', this.handleDBCardClick)
        this.handledecklistClick = this.decklistClick.bind(this)
        $('.decklist-area').on('click', 'img', this.handledecklistClick)
    }
    mDeckLength() {
        return this.decklist.mainDeck.length < this.mainLimit
    }
    eDeckLength() {
        return this.decklist.eggDeck.length < this.eggLimit
    }
    sDeckLength() {
        return this.decklist.sideDeck.length < this.sideLimit
    }
    checkInstancesOfCard(cardNum, isEgg) {
        const {cardLimit,decklist} = this
        
        if (isEgg) {
            const eggSideArry = decklist.eggDeck.concat(decklist.sideDeck)

            const eggCardCount = eggSideArry.filter(val => {
                return val === cardNum
            })

            return eggCardCount.length < cardLimit

        } else {
            const mainSideArry = decklist.mainDeck.concat(decklist.sideDeck)

            const mainCardCount = mainSideArry.filter(val => {
                return val === cardNum
            })

            return mainCardCount.length < cardLimit
        }
    }
    mainCardSorter(cardNum,cardData,isEgg) {
        const card = createCardHTML(cardData)

        if (isEgg) {
            if (!this.eDeckLength()) {
                console.log('Deck can have only 5 egg cards.')
            } else {
                this.decklist.eggDeck.push(cardNum)
                let count = parseInt($('#ED-count').html())
                count ++;
                $('#ED-count').html(count)
                $('.egg-deck').append(card)
            }
        } else {
            if (!this.mDeckLength()) {
                console.log('Deck can have only 50 main cards.')
            } else {
                this.decklist.mainDeck.push(cardNum)
                let count = parseInt($('#MD-count').html())
                count ++;
                $('#MD-count').html(count)
                $('.main-deck').append(card)
            }
        }
    }
    sideCardSorter(cardNum,cardData) {
        const card = createCardHTML(cardData)

        if (!this.sDeckLength()) {
            console.log('Deck can have only 10 side cards.')
        } else {
            this.decklist.sideDeck.push(cardNum)
            let count = parseInt($('#SD-count').html())
            count ++;
            $('#SD-count').html(count)
            $('.side-deck').append(card)            
        }
    }
    removeCard(cardNum, deckType) {
        if (deckType === 'main') {
            const idx =  this.decklist.mainDeck.indexOf(cardNum)
            let count = parseInt($('#MD-count').html())
            count --;
            $('#MD-count').html(count)
            return this.decklist.mainDeck.splice(idx,1)
        }
        if (deckType === 'egg') {
            const idx =  this.decklist.eggDeck.indexOf(cardNum)
            let count = parseInt($('#ED-count').html())
            count --;
            $('#ED-count').html(count)
            return this.decklist.eggDeck.splice(idx,1)
        }
        if (deckType === 'side') {
            const idx =  this.decklist.sideDeck.indexOf(cardNum)
            let count = parseInt($('#SD-count').html())
            count --;
            $('#SD-count').html(count)
            return this.decklist.sideDeck.splice(idx,1)
        }
    }
    async handleClick(e) {
        const cardNum = $(e.target).closest('div').attr('data-card-num')

        const cardData = await axios.patch(`/cards/${cardNum}`).then(resp => {
            return resp.data
        }).catch(err => {
            console.log(err)
        })

        const isEgg = cardData.type === 'Digi-Egg'

        if (!this.checkInstancesOfCard(cardNum,isEgg)) {
            console.log('Can have only 4 of any 1 card between main/egg and side decks.')
        } else {
            if ($('#card-sorter').val() === 'main') {
                this.mainCardSorter(cardNum,cardData,isEgg)
            } else {
                this.sideCardSorter(cardNum,cardData)
            }
        }
    }
    decklistClick(e) {
        const cardNum = $(e.target).closest('div').attr('data-card-num')

        const deckType = $(e.target).closest('li').attr('data-deck-type')

        this.removeCard(cardNum,deckType)
        $($(e.target).parent().remove())
    }
}

