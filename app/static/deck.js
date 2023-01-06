// Deck class for deck builder.

class Deck {
    constructor(mainLimit,eggLimit,sideLimit,cardLimit) {
        this.mainLimit = mainLimit
        this.eggLimit = eggLimit
        this.sideLimit = sideLimit
        this.cardLimit = cardLimit
        this.decklist = {
            mainDeck: {},
            eggDeck: {},
            sideDeck: {}
        }
    }
    startDB() {
        $('#search-button').addClass('d-none')

        this.handleDBCardClick = this.handleClick.bind(this)
        $('.db-search-results').on('click','img', this.handleDBCardClick)

        this.handledecklistClick = this.decklistClick.bind(this)
        $('.decklist-area').on('click', 'img', this.handledecklistClick)

        this.handleClearMain = this.clearMainDeck.bind(this)
        $('#clear-main').on('click', this.handleClearMain)

        this.handleSave = this.saveDeck.bind(this)
        $('#save-deck').on('submit', this.handleSave)
    }
    sumCards = (obj) => {
        return Object.values(obj).reduce((a,b) => a + b, 0)
    }
    mDeckLength() {
        return this.sumCards(this.decklist.mainDeck) < this.mainLimit
    }
    eDeckLength() {
        return this.sumCards(this.decklist.eggDeck) < this.eggLimit
    }
    sDeckLength() {
        return this.sumCards(this.decklist.sideDeck) < this.sideLimit
    }
    toastHTML(msg) {
        return `
        <div class="p-3" style="z-index: 2">
            <div class="toast show bg-warning" role="alert">
                <div class="toast-header bg-warning text-dark">
                <i class="fa-solid fa-gear p-1"></i> 
                <strong class="me-auto">DigimonCard</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${msg}
                </div>
            </div>
        </div>
        `
    }
    showToast(toastMsg, msg) {
        if ($('.toast-container').has('div').length) {
            const toasts = $('.toast-body').html()

            if (!toasts.includes(msg)) {
                $('.toast-container').append(toastMsg)
    
                setTimeout((() => {
                    $('.toast-container').children().first().remove()
                }), 5000)
            } else {
                return
            }
        } else {
            $('.toast-container').append(toastMsg)
    
                setTimeout((() => {
                    $('.toast-container').children().first().remove()
                }), 5000)
        }
    }
    checkInstancesOfCard(cardNum, isEgg) {
        const {cardLimit,decklist} = this

        let sideDeckCount = decklist.sideDeck[`${cardNum}`] || 0
        let eggCardCount = decklist.eggDeck[`${cardNum}`] || 0
        let mainCardCount = decklist.mainDeck[`${cardNum}`] || 0
        
        if (isEgg) {
            if (sideDeckCount) {
                sideDeckCount += eggCardCount
                return sideDeckCount < cardLimit
            } else {
                eggCardCount += sideDeckCount
                return eggCardCount < cardLimit
            }
        } else {
            if (sideDeckCount) {
                sideDeckCount += mainCardCount
                return sideDeckCount < cardLimit
            } else {
                mainCardCount += sideDeckCount
                return mainCardCount < cardLimit
            }
        }
    }
    mainCardSorter(cardNum,cardData,isEgg) {
        const card = createCardHTML(cardData)

        if (isEgg) {
            if (!this.eDeckLength()) {
                const msg = 'Deck can have only 5 egg cards.'
                const toastMsg = this.toastHTML(msg)

                this.showToast(toastMsg,msg)
            } else {
                const eDeck = this.decklist.eggDeck
                eDeck[`${cardNum}`] = eDeck[`${cardNum}`] + 1 || 1;
                let count = parseInt($('#ED-count').html())
                count ++;
                $('#ED-count').html(count)
                $('.egg-deck').append(card)
            }
        } else {
            if (!this.mDeckLength()) {
                const msg = 'Deck can have only 50 main cards.'
                const toastMsg = this.toastHTML(msg)

                this.showToast(toastMsg,msg)
            } else {
                const mDeck = this.decklist.mainDeck
                mDeck[`${cardNum}`] = mDeck[`${cardNum}`] + 1 || 1;
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
            const msg = 'Deck can have only 10 side cards.'
            const toastMsg = this.toastHTML(msg)

            this.showToast(toastMsg, msg)
        } else {
            const sDeck = this.decklist.sideDeck
            sDeck[`${cardNum}`] = sDeck[`${cardNum}`] + 1 || 1;
            let count = parseInt($('#SD-count').html())
            count ++;
            $('#SD-count').html(count)
            $('.side-deck').append(card)            
        }
    }
    removeCard(cardNum, deckType) {

        const DL =  this.decklist[`${deckType}`]

        if (DL[`${cardNum}`] > 0) {
            DL[`${cardNum}`] -= 1;

            if (deckType === 'mainDeck') {
                let count = parseInt($('#MD-count').html())
                count --
                $('#MD-count').html(count)
            }
            if (deckType === 'eggDeck') {
                let count = parseInt($('#ED-count').html())
                count --
                $('#ED-count').html(count)
            }
            if (deckType === 'sideDeck') {
                let count = parseInt($('#SD-count').html())
                count --
                $('#SD-count').html(count)
            }
        }
        if (DL[`${cardNum}`] === 0) {
            return delete DL[`${cardNum}`]
        }
    }
    clearMainDeck(e) {
        e.preventDefault();
        $('#MD-count').html('0');
        $('.main-deck').empty();
        const mDeck = this.decklist.mainDeck

        for (let cardNum in mDeck) {
            delete mDeck[cardNum]
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
            const msg = 'Can have only 4 copies of any one card between Main/Egg and Side decks.'
            const toastMsg = this.toastHTML(msg)

            this.showToast(toastMsg, msg)
            
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
    startNewDB = () => {
        clearForm()
        $('#MD-count').html('0');
        $('#ED-count').html('0');
        $('#SD-count').html('0');
        $('.decklist-area').empty();
        $('input[name="n"]').focus()

        const MD = this.decklist.mainDeck
        const ED = this.decklist.eggDeck
        const SD = this.decklist.sideDeck

        for (let cardNum in MD) {
            delete MD[cardNum]
        }
        for (let cardNum in ED) {
            delete ED[cardNum]
        }
        for (let cardNum in SD) {
            delete SD[cardNum]
        }
    }
    createDeckHTML = (newDeckResp) => {
        const deck = newDeckResp.deck
        
        return `
        <li class="row justify-content-center rounded m-2 search-card-img">
            <div class="card col-12 p-0 text-center">
                <img src="${deck.HDP_deck_img}" alt="" class="card-img-top">
                <a href="/decks/${deck.id}" class="text-light card-img-overlay rounded">
                    ${deck.name}
                </a>
            </div>
        </li>
        `
    }
    async saveDeck(e) {
        e.preventDefault();

        const data = {
            name: $('#deck-name').val(),
            decklist: this.decklist
        }

        const main_total = this.sumCards(this.decklist.mainDeck)

        if (main_total === this.mainLimit && data.name) {
            await axios({
                    method: 'post',
                    url: '/decks',
                    data: data
            }).then((resp) => {
                const newDeck = this.createDeckHTML(resp.data)
                $('#no-decks').remove()
                $('#list-decks').append(newDeck)
                this.startNewDB()
            }).catch((err) => {
                console.log(err)
            })
        } else {
            if (!data.name) {
                const msg = 'Enter a deck name.'
                const toastMsg = this.toastHTML(msg)

                this.showToast(toastMsg, msg)
            } 
            if (main_total != this.mainLimit) {
                const msg = 'Main Deck must have 50 cards.'
                const toastMsg = this.toastHTML(msg)

                this.showToast(toastMsg, msg)
            }
        }
    }
}