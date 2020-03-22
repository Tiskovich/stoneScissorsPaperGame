Vue.component('counter', {
                        data: function () {
                            return {
                            max_count: 5
                            }
                    },
                    methods: {
                            count() {
                                let timerId = setTimeout(function tick(count) {
                                if (this.count >= 1000) {
                                    this.count--;
                                    timerId = setTimeout(tick, 1000, this.count);}
                                }, 1000, this.count);
                            }
                    },
                    template: '<div class="counter" ref="child">{{ max_count }}</div>'
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
                    console.log(symbol)
                    console.log('Send' + '"' + symbol + '"' +'to opponents...');
                    var room = localStorage.getItem('room');
                    socket.emit('game_move', {size: 2, symbol: symbol, room: room});
                    this.isGameCreated = !this.isGameCreated
        },
        exec() {
        this.$refs.child.count()
        }
    }
});



var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('join_room', function(msg) {
        console.log(msg);
        localStorage.setItem('room', msg.room);
        app.isGameCreated = true;
        app.exec();
        });

socket.on('game_res', function(msg) {
        console.log(msg);
        app.isGameCreated = false;
        app.isResults = true;
        app.results = msg;
    });