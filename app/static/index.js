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
        player_name: '',
        room: '',
        size: 2,
        player_sid: '',
    },
    methods: {
        createGame() {
                    this.isStartGame = !this.isStartGame
                    socket.on('connect', function() {
                    console.log('Websocket connected!');
                    });
                    console.log(this.player_name)
                    socket.emit('create', {size: 2, player_name: this.player_name});
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
        games_counter: function () {
            var total = 0;
            for (key in this.results['stats']) {
                total += this.results['stats'][key];
            };
            console.log(total);
            return total
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