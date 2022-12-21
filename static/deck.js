// Deck class

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
    mDeckLength() {
        return sumCards(this.decklist.mainDeck) < this.mainLimit
    }
    eDeckLength() {
        return sumCards(this.decklist.eggDeck) < this.eggLimit
    }
    sDeckLength() {
        return sumCards(this.decklist.sideDeck) < this.sideLimit
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
                console.log('Deck can have only 5 egg cards.')
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
                console.log('Deck can have only 50 main cards.')
            } else {
                const mDeck = this.decklist.mainDeck
                mDeck[`${cardNum}`] = mDeck[`${cardNum}`] + 1 || 1;
                let count = parseInt($('#MD-count').html())
                count ++;
                $('#MD-count').html(count)
                $('.main-deck').append(card)
            }
        }
        console.log(this.decklist)
    }
    sideCardSorter(cardNum,cardData) {
        const card = createCardHTML(cardData)

        if (!this.sDeckLength()) {
            console.log('Deck can have only 10 side cards.')
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
    startNewDB = () => {
        clearForm()
        $('#MD-count').html('0');
        $('#ED-count').html('0');
        $('#SD-count').html('0');
        $('.decklist-area').empty();

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
    async saveDeck(e) {
        e.preventDefault();

        const data = {
            name: $('#deck-name').val(),
            decklist: this.decklist
        }

        if (sumCards(this.decklist.mainDeck) === 50) {
            const newDeckResp = await axios({
                    method: 'post',
                    url: '/decks',
                    data: data
            }).then((resp) => {
                return resp.data
            }).catch((err) => {
                console.log(err)
            })

            const newDeck = createDeckHTML(newDeckResp)
            $('#list-decks').append(newDeck)
            
            this.startNewDB()

        } else {
            console.log('Main Deck must have 50 cards.')
        }
    }
}