Vue.component('timer', {
                        data: function () {
                            return {
                            start_count: 5,
                            end_count: 0,
                            timerId: ''
                            };
                    },
                    mounted() {
                        var self = this;
                        this.timerId = setInterval(function () {
                            self.timer_count(self.start_count, self.end_count);
                            }, 1000);
                    },
                    beforeDestroy() {
                         clearInterval(this.timerId)
                    },
                    methods: {
                        timer_count(start_count, end_count) {
                        if (start_count > end_count) {
                            this.start_count = this.start_count - 1;
                        } else {
                            this.$root.sendSymbol('inactive');
                            clearInterval(this.timerId)
                        }
                    },
                },
                    template: '<div class="timer"><p>{{start_count}}</p></div>',
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