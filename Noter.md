### Flask based chess-engine

In this project we will follow the video-series ```https://www.youtube.com/watch?v=_0uKZbHWVKM&list=PLmN0neTso3Jz-6--Mj51Hc3jiLhkQm0DB```
to make a flask-based chess-engine, and try to deploy it.  

First step will be to create this note, and create a git repository.

```bash
PS C:\src\egne projekter\Docker-chess\flask based version> git init
Initialized empty Git repository in C:/src/egne projekter/Docker-chess/flask based version/.git/
PS C:\src\egne projekter\Docker-chess\flask based version> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        Noter.md

nothing added to commit but untracked files present (use "git add" to track)
PS C:\src\egne projekter\Docker-chess\flask based version> git add *
PS C:\src\egne projekter\Docker-chess\flask based version> git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   Noter.md

PS C:\src\egne projekter\Docker-chess\flask based version> git commit
[master (root-commit) b96c401] Initial commit
 1 file changed, 6 insertions(+)
 create mode 100644 Noter.md
PS C:\src\egne projekter\Docker-chess\flask based version> git status
On branch master
nothing to commit, working tree clean
PS C:\src\egne projekter\Docker-chess\flask based version>
```

### Technologies used
- chessboard.js for view.
- flask for webserver
- chessboard.js for chess-logic in frontend
-  python-chess for backend chess logic

### General structure

In the backend we essentially have a an endpoint called `/make_move` which simply receives the fen of the game as follows
```python
@app.route
def make_move():
    fen = request.form.get('data')
    board = chess.board(fen)
    info=engine.play(board)
    board.push(info.move)
    return board.fen()
```

Essentially this endpoint is being hit from the frontend using the code
```js
function onDrop(source, target){
    ...

    $.post(/make_move, {data:game.fen},function(fen){
        game.load(fen)
        board.position(fen)
        if(game.game_over()){
            updateStatus()
        }
    } )
}
```

### Detailed implementation

We will start by setting up a docker-container to hold our app. For the moment we are not planning on actually pushing the docker container, so we will start by simply running docker manually

```Dockerfile
FROM ubuntu:latest
EXPOSE 80
LABEL author="Anders Kølvraa"
USER root
# needed for update
RUN apt-get update 
# -y needed to avoid prompting whether to continue.
RUN apt-get install -y python3.11
```
We build this contaienr with
``` docker build . -t flask-chess```

Since we cannot mount a directory in the docker-file we will do this when runnign the container.

```bash
docker run -p 80:80 --mount type=bind,source='C:\src\egne projekter\Docker-chess\flask based version\containerdirectory',target=/home/chess -it flask-chess
```

BEMÆRK: Vi har inkluderet `-it` ovenfor da vi ellers bare kører vores docker contaiern hvorefter den exiter.

Now install pip ` apt install python3-pip` and flask `pip install flask` and python-chess `pip install python-chess`.

` apt-get install python3.11-venv`

Note that in order to get our flask-app to run in docker we have to set host to '0.0.0.0' i.e. all ip-adresses/network-interfaces used by teh contaienr.  This is because a docker container apparently uses multiple network-interfaces. To verify this lets list the ip-adresses in our contaienr. This is done by the command `ip addr`, but unfortunately our ubuntu base image doesnt know this command. To find wich program should be installed to run a given package, we first install `apt-file`, and then run
```apt-file search --regexp 'bin/ip$'```
This will display `iproute2`, and after installing this we find
```r
root@07ab3cca5528:/# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/ipip 0.0.0.0 brd 0.0.0.0
3: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/sit 0.0.0.0 brd 0.0.0.0
48: eth0@if49: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```
Apparently localhost (127.0.0.1) is different form the external ipadress (instead of catch-all we could also specifically use the ip whihc our container uses on the bridge network). Running `docker network list` we see the networks, and running `docker network inspect bridge` we see the ip-adresses connected to the bridge.
IT seems that with `docker run` you can specify `--network bridge` og `--network host`, where bridge requires port-mapping whereas host doesnt. It seems that docker starts both networks simultanously.

After a few startup-trouble we can not reproduce what we need - and by pointing teh 'piecetheme'-link to the img folder in static, we get something which works.


We will install a stockfish engine with `apt get stockfish`. herefter vil stockfish være installeret i `/usr/games/stockfish` hvorfra den kan startes som uci. En eksempel sessoin kunne være 
```r
root@07ab3cca5528:/usr/games# ./stockfish
Stockfish 14.1 by the Stockfish developers (see AUTHORS file)
board
Unknown command: board
uci
id name Stockfish 14.1
id author the Stockfish developers (see AUTHORS file)

option name Debug Log File type string default
option name Threads type spin default 1 min 1 max 512
option name Hash type spin default 16 min 1 max 33554432
option name Clear Hash type button
option name Ponder type check default false
option name MultiPV type spin default 1 min 1 max 500
option name Skill Level type spin default 20 min 0 max 20
option name Move Overhead type spin default 10 min 0 max 5000
option name Slow Mover type spin default 100 min 10 max 1000
option name nodestime type spin default 0 min 0 max 10000
option name UCI_Chess960 type check default false
option name UCI_AnalyseMode type check default false
option name UCI_LimitStrength type check default false
option name UCI_Elo type spin default 1350 min 1350 max 2850
option name UCI_ShowWDL type check default false
option name SyzygyPath type string default <empty>
option name SyzygyProbeDepth type spin default 1 min 1 max 100
option name Syzygy50MoveRule type check default true
option name SyzygyProbeLimit type spin default 7 min 0 max 7
option name Use NNUE type check default true
option name EvalFile type string default nn-13406b1dcbe0.nnue
uciok
isready
readyok
ucinewgame
isready
readyok
depth 9 go
Unknown command: depth 9 go
go depth 9
info string NNUE evaluation using nn-13406b1dcbe0.nnue enabled
info depth 1 seldepth 1 multipv 1 score cp 38 nodes 20 nps 20000 tbhits 0 time 1 pv d2d4
info depth 2 seldepth 2 multipv 1 score cp 82 nodes 51 nps 51000 tbhits 0 time 1 pv e2e4 a7a6
info depth 3 seldepth 3 multipv 1 score cp 55 nodes 154 nps 154000 tbhits 0 time 1 pv e2e4 c7c6 d2d4
info depth 4 seldepth 4 multipv 1 score cp 22 nodes 807 nps 403500 tbhits 0 time 2 pv g1f3 d7d5 d2d4 g8f6
info depth 5 seldepth 5 multipv 1 score cp 54 nodes 1061 nps 353666 tbhits 0 time 3 pv e2e4 c7c5 g1f3
info depth 6 seldepth 6 multipv 1 score cp 54 nodes 1761 nps 440250 tbhits 0 time 4 pv e2e4 c7c5 g1f3 d7d5 e4d5 d8d5
info depth 7 seldepth 8 multipv 1 score cp 50 nodes 5459 nps 606555 tbhits 0 time 9 pv e2e4 e7e5 g1f3 b8c6 b1c3 g8f6 d2d4
info depth 8 seldepth 8 multipv 1 score cp 50 nodes 6998 nps 699800 tbhits 0 time 10 pv e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 g8f6 b1c3
info depth 9 seldepth 11 multipv 1 score cp 54 nodes 12053 nps 634368 tbhits 0 time 19 pv e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 g8f6 d4c6
bestmove e2e4 ponder e7e5
```


To monitor pipe-communication between app.py and stockfish we will try to use strace. 
Start with `apt-get install strace`. Now setting `strace -p 5626` will give stdin with the relevant uci-commands. Bedre lader til at være `strace -fp <pid>` da vi isåfald både får `read`(dvs STDIN) og `write`(dvs STDOUT).
Best of all is probably the following version:
` strace -fp 5626 -e trace=read -e trace=write -v -s 150 2>&1 | tee strace.log`
where I have used `-e trace=read` to only outout read (and write) commands, I have used `-v -s 150` to set the stringlimit for 150 instead of the default of 32, I have set `2>&1` since apparently strace outputs to STDERR by default, and thsi should be redirected, and finally we use `tee` to write output to file. This should allow us to monitor what is written through our pipe, and hence be able to reproduce this in our chess-engine.

Installing numpy as well, to use in the minimaxbot.

In order to actually run our flask webapp we need to first start the container, and then run the flask-app. The first is described how is done above, whereas the second is simply handled by 
```python3.10 -m app```