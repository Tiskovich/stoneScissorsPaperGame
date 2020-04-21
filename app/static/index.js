Vue.component('timer', {
    data: function () {
        return {
            timerId: ''
        };
    },
    props: ['start', 'end', 'fn'],
    mounted() {
        var self = this;
        this.timerId = setInterval(function () {
            self.count(self.start, self.end);
        }, 1000);
    },
    beforeDestroy() {
        clearInterval(this.timerId)
    },
    methods: {
        count(start, end) {
            if (start > end) {
                this.start = this.start - 1;
            } else {
                this.fn();
                clearInterval(this.timerId)
            }
        },
    },
    template: '<div class="timer">{{start}}</div>',
});

var app = new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: {
        isStartGame: true,
        isGameCreated: false,
        isResults: false,
        results: '',
        player_name: '',
        room: '',
        size: 2,
        player_sid: '',
        round: 1,
        start: 5,
        end: 0,
        waitNewGameStart: 4,
    },
    methods: {
        createGame(event, round = 1) {
            this.isStartGame = false;
            this.isGameCreated = false;
            this.isResults = false;
            socket.on('connect', function() {
                console.log('Websocket connected!');
            });
            console.log(round);
            socket.emit('create', {size: 2, player_name: this.player_name, round: round, room: this.room});
        },
        continueGame() {
            ++this.round;
            console.log('ROUND')
            console.log(this.round)
            this.createGame(this.round)
        },
        sendSymbol(symbol) {
            console.log(symbol);
            console.log('Send ' + '"' + symbol + '"' + ' to opponents...');
            socket.emit('game_move', {size: this.size, symbol: symbol, room: this.room, player_name: this.player_name});
            this.isGameCreated = !this.isGameCreated;
        },
        exitGame() {
            socket.emit('terminate_session', {player_sid: this.player_sid, room: this.room});
            console.log('Exit from current game');
            location.reload(true);
        }
    },
    computed: {
        gamesCounter: function () {
            var total = 0;
            for (key in this.results['stats']) {
                total += this.results['stats'][key];
            }
            console.log(total);
            return total
        },
        newRound: function () {
            return this.results['your_results'] == 2;
        }
    }
});



var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('join_room', function(msg) {
    console.log(msg);
    app.room =  msg.room;
    app.player_sid = msg.player_sid;
    app.isGameCreated = true;
    app.results = msg.results;
});

socket.on('game_res', function(msg) {
    console.log(msg);
    app.isGameCreated = false;
    app.isResults = true;
    app.results = msg;
});