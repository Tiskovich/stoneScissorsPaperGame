Vue.component('counter', {
                        data: function () {
                            return {
                            max_count: 5
                            }
                    },
                    methods: {
                            count: function () {
                                var self = this;
                                let timerId = setTimeout(function tick(count) {
                                if (self.count >= 1000) {
                                    self.count--;
                                    timerId = setTimeout(tick, 1000, self.count);}
                                }, 1000, self.count);
                            }
                    },
                    template: '<div class="counter">[[max_count]]</div>'
})

var app = new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: {
        isStartGame: true,
        isGameCreated: false,
        isResults: false,
        results: '',
    },
    methods: {
        createGame() {
                    this.isStartGame = !this.isStartGame
                    socket.on('connect', function() {
                    console.log('Websocket connected!');
                    });
                    socket.emit('create', {size: 2});
        },
        sendSymbol(symbol) {
                    console.log(symbol);
                    console.log('Send' + '"' + symbol + '"' +'to opponents...');
                    var room = localStorage.getItem('room');
                    socket.emit('game_move', {size: 2, symbol: symbol, room: room});
                    this.isGameCreated = !this.isGameCreated;
        },
        exitGame() {
            var room = localStorage.getItem('room');
            socket.emit('terminate_session', {player_id: localStorage.getItem('player_id'), room:  localStorage.getItem('room')});
            console.log('Exit from current game');
            location.reload(true);
        }
    }
});



var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('join_room', function(msg) {
        console.log(msg);
        localStorage.setItem('room', msg.room);
        localStorage.setItem('player_id', msg.player_id);
        app.isGameCreated = true;
//        app.count();
        });

socket.on('game_res', function(msg) {
        console.log(msg);
        if (msg.your_choice == 'dead_heat' || msg.opponent_choices.includes('dead_heat')) {
            app.isGameCreated = true;
        } else {
            app.isGameCreated = false;
            app.isResults = true;
            app.results = msg;
                }
    });