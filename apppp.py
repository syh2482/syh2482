import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Bounce",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Bounce</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            touch-action: none;
        }
        #game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        canvas {
            background-color: #1e293b;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.25);
            border-radius: 12px;
            max-width: 98%;
            max-height: 82vh;
            image-rendering: pixelated;
        }
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .header {
            display: flex;
            justify-content: space-between;
            padding: 16px 24px;
            font-size: 1.25rem;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.92);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            pointer-events: auto;
            z-index: 10;
        }
        .overlay-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            color: #38bdf8;
            text-shadow: 0 0 20px #38bdf8, 0 0 40px #0284c7;
            text-align: center;
            line-height: 1.1;
        }
        .btn {
            background: linear-gradient(135deg, #0ea5e9, #2563eb);
            color: white;
            border: none;
            padding: 14px 36px;
            font-size: 1.15rem;
            font-weight: 600;
            border-radius: 9999px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            transition: transform 0.1s, box-shadow 0.1s;
            margin: 8px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }
        .btn:active {
            transform: translateY(2px);
        }
        .hidden {
            display: none !important;
        }
        #mobile-controls {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 600px;
            padding: 16px 24px;
            pointer-events: auto;
            margin-top: auto;
        }
        .control-btn {
            width: 70px;
            height: 70px;
            background: rgba(56, 189, 248, 0.2);
            border: 2px solid rgba(56, 189, 248, 0.5);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            color: rgba(255, 255, 255, 0.85);
            user-select: none;
            -webkit-user-select: none;
        }
        .control-btn:active {
            background: rgba(56, 189, 248, 0.5);
        }
        @media (min-width: 768px) {
            #mobile-controls {
                display: none;
            }
            canvas {
                max-height: 88vh;
            }
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas"></canvas>
        
        <div id="ui-layer">
            <div class="header">
                <span id="stage-display">Stage 1</span>
                <span id="dash-display" style="color: #94a3b8;">Dash: NONE</span>
                <span id="deaths-display">Deaths: 0</span>
            </div>
            
            <div id="mobile-controls">
                <div class="control-btn" id="btn-left">◀</div>
                <div class="control-btn" id="btn-dash" style="font-size:1.1rem; font-weight:bold;">DASH</div>
                <div class="control-btn" id="btn-right">▶</div>
            </div>
        </div>

        <!-- 메인 메뉴 -->
        <div id="main-menu" class="overlay">
            <div class="overlay-title">NEON<br>BOUNCE</div>
            <button class="btn" id="start-btn">Game Start</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Start</p>
            <p class="mt-1 text-slate-500 text-sm">Move: A/D or Arrow Keys | Dash: Shift / X</p>
        </div>

        <!-- 게임 오버 -->
        <div id="game-over" class="overlay hidden">
            <div class="overlay-title" style="color: #ef4444; text-shadow: 0 0 20px #ef4444, 0 0 40px #b91c1c;">GAME OVER</div>
            <button class="btn" id="retry-btn">Retry Stage</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Retry</p>
        </div>

        <!-- 스테이지 클리어 -->
        <div id="stage-clear" class="overlay hidden">
            <div class="overlay-title" style="color: #4ade80; text-shadow: 0 0 20px #4ade80, 0 0 40px #16a34a;">STAGE CLEAR!</div>
            <button class="btn" id="next-btn">Next Stage</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Next</p>
        </div>
        
        <!-- 올 클리어 -->
        <div id="all-clear" class="overlay hidden">
            <div class="overlay-title" style="color: #facc15; text-shadow: 0 0 20px #facc15, 0 0 40px #ca8a04;">ALL CLEAR!</div>
            <p id="final-stats" class="mb-6 text-2xl font-bold">Total Deaths: 0</p>
            <button class="btn" id="home-btn">Main Menu</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Menu</p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const uiStage = document.getElementById('stage-display');
        const uiDeaths = document.getElementById('deaths-display');
        const uiDash = document.getElementById('dash-display');
        const mainMenu = document.getElementById('main-menu');
        const gameOverScreen = document.getElementById('game-over');
        const stageClearScreen = document.getElementById('stage-clear');
        const allClearScreen = document.getElementById('all-clear');
        const finalStats = document.getElementById('final-stats');

        const TILE_SIZE = 40; 
        const COLS = 20;
        const ROWS = 15;
        const GAME_WIDTH = COLS * TILE_SIZE; 
        const GAME_HEIGHT = ROWS * TILE_SIZE; 
        
        let scale = 1;

        const COLORS = {
            BG: '#0f172a',
            GRID: '#1e293b',
            PLAYER: '#38bdf8',
            PLAYER_GLOW: '#0284c7',
            BLOCK: 'rgba(148, 163, 184, 0.8)',
            BLOCK_BORDER: '#cbd5e1',
            SPIKE: '#ef4444',
            SPIKE_GLOW: '#b91c1c',
            GOAL: '#4ade80',
            GOAL_GLOW: '#16a34a',
            DASH_GLOW: '#ec4899'
        };

        let gameState = 'menu';
        let currentStage = 0;
        let deaths = 0;
        let animationId;
        
        const keys = {
            ArrowLeft: false,
            ArrowRight: false,
            a: false,
            d: false,
            Shift: false,
            x: false
        };

        let touchLeft = false;
        let touchRight = false;
        let touchDash = false;

        class Player {
            constructor(x, y) {
                this.startX = x;
                this.startY = y;
                this.x = x;
                this.y = y;
                this.radius = TILE_SIZE * 0.35;
                this.vx = 0;
                this.vy = 0;
                this.speed = TILE_SIZE * 0.15;
                this.gravity = TILE_SIZE * 0.02;
                this.bounceForce = -TILE_SIZE * 0.35;
                
                this.trail = [];
                this.hasDashItem = false;
                this.dashTimer = 0;
                this.isDashing = false;
                this.facingDir = 1;
            }

            reset() {
                this.x = this.startX;
                this.y = this.startY;
                this.vx = 0;
                this.vy = 0;
                this.trail = [];
                this.hasDashItem = false;
                this.dashTimer = 0;
                this.isDashing = false;
            }

            triggerDash() {
                if (this.hasDashItem && !this.isDashing) {
                    this.isDashing = true;
                    this.dashTimer = 10;
                    this.hasDashItem = false;
                }
            }

            update() {
                let isMovingLeft = keys.ArrowLeft || keys.a || touchLeft;
                let isMovingRight = keys.ArrowRight || keys.d || touchRight;

                if (isMovingLeft) {
                    this.vx = -this.speed;
                    this.facingDir = -1;
                } else if (isMovingRight) {
                    this.vx = this.speed;
                    this.facingDir = 1;
                } else {
                    this.vx = 0;
                }

                if (keys.Shift || keys.x || touchDash) {
                    this.triggerDash();
                    touchDash = false;
                }

                if (this.isDashing) {
                    this.vx = this.facingDir * (this.speed * 3.2);
                    this.vy = 0;
                    this.dashTimer--;
                    if (this.dashTimer <= 0) {
                        this.isDashing = false;
                    }
                } else {
                    this.vy += this.gravity;
                    if (this.vy > TILE_SIZE * 0.4) this.vy = TILE_SIZE * 0.4;
                }

                this.x += this.vx;
                this.y += this.vy;

                this.trail.push({ x: this.x, y: this.y });
                if (this.trail.length > 8) this.trail.shift();

                if (this.y - this.radius > GAME_HEIGHT) {
                    die();
                }
            }

            draw(ctx) {
                for (let i = 0; i < this.trail.length; i++) {
                    let p = this.trail[i];
                    let alpha = (i + 1) / this.trail.length * 0.4;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, this.radius * 0.8, 0, Math.PI * 2);
                    ctx.fillStyle = this.isDashing ? COLORS.DASH_GLOW : COLORS.PLAYER;
                    ctx.globalAlpha = alpha;
                    ctx.fill();
                }
                ctx.globalAlpha = 1.0;

                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius * 1.3, 0, Math.PI * 2);
                ctx.fillStyle = this.isDashing ? COLORS.DASH_GLOW : COLORS.PLAYER_GLOW;
                ctx.globalAlpha = 0.5;
                ctx.fill();
                ctx.globalAlpha = 1.0;

                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = COLORS.PLAYER;
                ctx.fill();

                ctx.beginPath();
                ctx.arc(this.x - this.radius * 0.3, this.y - this.radius * 0.3, this.radius * 0.2, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(255,255,255,0.6)';
                ctx.fill();
            }
        }

        const BLOCK_TYPES = {
            EMPTY: 0, 
            NORMAL: 1, 
            SPIKE_UP: 2, 
            SPIKE_DOWN: 3, 
            SPIKE_LEFT: 4, 
            SPIKE_RIGHT: 5, 
            MOVING_HORIZ: 6,
            MOVING_VERT: 7,
            PLAYER_START: 8, 
            GOAL: 9,
            DASH_ITEM: 10
        };

        class Block {
            constructor(x, y, type) {
                this.startX = x * TILE_SIZE;
                this.startY = y * TILE_SIZE;
                this.x = this.startX;
                this.y = this.startY;
                this.width = TILE_SIZE;
                this.height = TILE_SIZE;
                this.type = type;
                this.isCollected = false;
                
                this.moveRange = TILE_SIZE * 3;
                this.moveSpeed = 1.5;
                this.moveDir = 1;
            }

            update() {
                if (this.type === BLOCK_TYPES.MOVING_HORIZ) {
                    this.x += this.moveSpeed * this.moveDir;
                    if (Math.abs(this.x - this.startX) > this.moveRange) {
                        this.moveDir *= -1;
                    }
                } else if (this.type === BLOCK_TYPES.MOVING_VERT) {
                    this.y += this.moveSpeed * this.moveDir;
                    if (Math.abs(this.y - this.startY) > this.moveRange) {
                        this.moveDir *= -1;
                    }
                }
            }

            draw(ctx) {
                if (this.type === BLOCK_TYPES.NORMAL || this.type === BLOCK_TYPES.MOVING_HORIZ || this.type === BLOCK_TYPES.MOVING_VERT) {
                    ctx.fillStyle = this.type === BLOCK_TYPES.NORMAL ? '#64748b' : '#38bdf8';
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    ctx.strokeStyle = COLORS.BLOCK_BORDER;
                    ctx.lineWidth = 2;
                    ctx.strokeRect(this.x, this.y, this.width, this.height);
                } else if (this.type >= 2 && this.type <= 5) {
                    this.drawSpike(ctx);
                } else if (this.type === BLOCK_TYPES.GOAL) {
                    let cx = this.x + this.width / 2;
                    let cy = this.y + this.height / 2;
                    let r = this.width * 0.4;
                    
                    ctx.beginPath();
                    ctx.arc(cx, cy, r * 1.3, 0, Math.PI * 2);
                    ctx.fillStyle = COLORS.GOAL_GLOW;
                    ctx.globalAlpha = 0.5;
                    ctx.fill();
                    ctx.globalAlpha = 1.0;
                    
                    ctx.beginPath();
                    ctx.arc(cx, cy, r, 0, Math.PI * 2);
                    ctx.fillStyle = COLORS.GOAL;
                    ctx.fill();
                } else if (this.type === BLOCK_TYPES.DASH_ITEM && !this.isCollected) {
                    let cx = this.x + this.width / 2;
                    let cy = this.y + this.height / 2;
                    let time = Date.now() / 150;
                    cy += Math.sin(time) * 4;

                    ctx.beginPath();
                    ctx.arc(cx, cy, this.width * 0.4, 0, Math.PI * 2);
                    ctx.fillStyle = COLORS.DASH_GLOW;
                    ctx.globalAlpha = 0.4 + Math.sin(time * 0.5) * 0.2;
                    ctx.fill();
                    ctx.globalAlpha = 1.0;

                    ctx.beginPath();
                    ctx.moveTo(cx, cy - 12);
                    ctx.lineTo(cx + 12, cy);
                    ctx.lineTo(cx, cy + 12);
                    ctx.lineTo(cx - 12, cy);
                    ctx.closePath();
                    ctx.fillStyle = '#fbcfe8';
                    ctx.fill();
                    ctx.strokeStyle = COLORS.DASH_GLOW;
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }
            }

            drawSpike(ctx) {
                let x = this.x, y = this.y, w = this.width, h = this.height;
                ctx.beginPath();
                if (this.type === BLOCK_TYPES.SPIKE_UP) {
                    ctx.moveTo(x, y + h); ctx.lineTo(x + w / 2, y); ctx.lineTo(x + w, y + h);
                } else if (this.type === BLOCK_TYPES.SPIKE_DOWN) {
                    ctx.moveTo(x, y); ctx.lineTo(x + w / 2, y + h); ctx.lineTo(x + w, y);
                } else if (this.type === BLOCK_TYPES.SPIKE_LEFT) {
                    ctx.moveTo(x + w, y); ctx.lineTo(x, y + h / 2); ctx.lineTo(x + w, y + h);
                } else if (this.type === BLOCK_TYPES.SPIKE_RIGHT) {
                    ctx.moveTo(x, y); ctx.lineTo(x + w, y + h / 2); ctx.lineTo(x, y + h);
                }
                ctx.closePath();
                ctx.fillStyle = COLORS.SPIKE;
                ctx.fill();
            }
        }

        function rectCircleColliding(circle, rect) {
            let closestX = Math.max(rect.x, Math.min(circle.x, rect.x + rect.width));
            let closestY = Math.max(rect.y, Math.min(circle.y, rect.y + rect.height));
            let distanceX = circle.x - closestX;
            let distanceY = circle.y - closestY;
            return (distanceX * distanceX + distanceY * distanceY) < (circle.radius * circle.radius);
        }

        const stages = [
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11100111001110011111","00000000000000000000","00000000000000000000","00000000000000000000"],
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11110001111000111111","11112221111222111111","11111111111111111111","00000000000000000000"],
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800a00000000000111","00000000000000000000","11110000000000111111","00000000000000000000","00000000000000000000","00000000000000000000"],
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800000000000000011","00000000000000000000","11110000600000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00000000000000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000007000000000","00800000000000000000","11110000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00000000000000001111","00000000000000000000","00000000006000000000","0000000000000a000000","00000000000000000000","00800060000000000000","11110000000000000000","11112222222222221111","11111111111111111111","00000000000000000000","00000000000000000000"]
        ];

        let player;
        let blocks = [];

        function resize() {
            scale = Math.min(window.innerWidth / GAME_WIDTH, window.innerHeight / GAME_HEIGHT) * 0.92;
            canvas.width = GAME_WIDTH * scale;
            canvas.height = GAME_HEIGHT * scale;
            ctx.scale(scale, scale);
        }

        function loadStage(stageIndex) {
            blocks = [];
            player = null;
            const layout = stages[stageIndex];
            
            for (let y = 0; y < layout.length; y++) {
                for (let x = 0; x < layout[y].length; x++) {
                    const type = parseInt(layout[y][x], 16);
                    if (type === BLOCK_TYPES.PLAYER_START) {
                        player = new Player(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2);
                    } else if (type !== BLOCK_TYPES.EMPTY) {
                        blocks.push(new Block(x, y, type));
                    }
                }
            }
            uiStage.innerText = `Stage ${stageIndex + 1}`;
            uiDeaths.innerText = `Deaths: ${deaths}`;
        }

        function gameLoop() {
            if (gameState !== 'playing') return;

            for (let block of blocks) block.update();
            player.update();

            if (player.hasDashItem) {
                uiDash.innerText = "Dash: AVAILABLE (Shift)";
                uiDash.style.color = "#ec4899";
            } else {
                uiDash.innerText = "Dash: NONE";
                uiDash.style.color = "#94a3b8";
            }

            let prevY = player.y - player.vy;
            let prevX = player.x - player.vx;

            for (let block of blocks) {
                if (block.type === BLOCK_TYPES.DASH_ITEM && block.isCollected) continue;

                if (rectCircleColliding(player, block)) {
                    if (block.type === BLOCK_TYPES.DASH_ITEM) {
                        block.isCollected = true;
                        player.hasDashItem = true;
                        continue;
                    }

                    if (block.type === BLOCK_TYPES.GOAL) {
                        clearStage();
                        return;
                    }
                    if (block.type >= 2 && block.type <= 5) {
                        die();
                        return;
                    }

                    if (block.type === BLOCK_TYPES.NORMAL || block.type === BLOCK_TYPES.MOVING_HORIZ || block.type === BLOCK_TYPES.MOVING_VERT) {
                        if (prevY + player.radius <= block.y + 6) {
                            player.y = block.y - player.radius;
                            player.vy = player.bounceForce;
                        } else if (prevY - player.radius >= block.y + block.height - 6) {
                            player.y = block.y + block.height + player.radius;
                            player.vy = 0;
                        } else {
                            if (prevX < block.x) player.x = block.x - player.radius;
                            else if (prevX > block.x + block.width) player.x = block.x + block.width + player.radius;
                        }
                    }
                }
            }

            ctx.fillStyle = COLORS.BG;
            ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

            ctx.strokeStyle = COLORS.GRID;
            ctx.lineWidth = 1;
            ctx.beginPath();
            for (let x = 0; x <= GAME_WIDTH; x += TILE_SIZE) {
                ctx.moveTo(x, 0); ctx.lineTo(x, GAME_HEIGHT);
            }
            for (let y = 0; y <= GAME_HEIGHT; y += TILE_SIZE) {
                ctx.moveTo(0, y); ctx.lineTo(GAME_WIDTH, y);
            }
            ctx.stroke();

            for (let block of blocks) block.draw(ctx);
            player.draw(ctx);

            animationId = requestAnimationFrame(gameLoop);
        }

        function startGame() {
            gameState = 'playing';
            currentStage = 0;
            deaths = 0;
            hideAllMenus();
            loadStage(currentStage);
            animationId = requestAnimationFrame(gameLoop);
        }

        function die() {
            gameState = 'gameover';
            deaths++;
            uiDeaths.innerText = `Deaths: ${deaths}`;
            gameOverScreen.classList.remove('hidden');
            cancelAnimationFrame(animationId);
        }

        function retryStage() {
            gameState = 'playing';
            hideAllMenus();
            player.reset();
            for (let block of blocks) {
                if (block.type === BLOCK_TYPES.DASH_ITEM) block.isCollected = false;
            }
            animationId = requestAnimationFrame(gameLoop);
        }

        function clearStage() {
            gameState = 'clear';
            cancelAnimationFrame(animationId);
            if (currentStage < stages.length - 1) {
                stageClearScreen.classList.remove('hidden');
            } else {
                gameState = 'allclear';
                finalStats.innerText = `Total Deaths: ${deaths}`;
                allClearScreen.classList.remove('hidden');
            }
        }

        function nextStage() {
            currentStage++;
            gameState = 'playing';
            hideAllMenus();
            loadStage(currentStage);
            animationId = requestAnimationFrame(gameLoop);
        }

        function hideAllMenus() {
            mainMenu.classList.add('hidden');
            gameOverScreen.classList.add('hidden');
            stageClearScreen.classList.add('hidden');
            allClearScreen.classList.add('hidden');
        }

        window.addEventListener('resize', resize);

        window.addEventListener('keydown', (e) => {
            if (keys.hasOwnProperty(e.key)) keys[e.key] = true;
            if (e.code === 'Space') {
                e.preventDefault();
                if (gameState === 'menu') startGame();
                else if (gameState === 'gameover') retryStage();
                else if (gameState === 'clear') nextStage();
                else if (gameState === 'allclear') {
                    hideAllMenus();
                    mainMenu.classList.remove('hidden');
                    gameState = 'menu';
                }
            }
        });

        window.addEventListener('keyup', (e) => {
            if (keys.hasOwnProperty(e.key)) keys[e.key] = false;
        });

        document.getElementById('btn-left').addEventListener('touchstart', (e) => { e.preventDefault(); touchLeft = true; });
        document.getElementById('btn-left').addEventListener('touchend', (e) => { e.preventDefault(); touchLeft = false; });
        document.getElementById('btn-right').addEventListener('touchstart', (e) => { e.preventDefault(); touchRight = true; });
        document.getElementById('btn-right').addEventListener('touchend', (e) => { e.preventDefault(); touchRight = false; });
        document.getElementById('btn-dash').addEventListener('touchstart', (e) => { e.preventDefault(); touchDash = true; });

        document.getElementById('start-btn').addEventListener('click', startGame);
        document.getElementById('retry-btn').addEventListener('click', retryStage);
        document.getElementById('next-btn').addEventListener('click', nextStage);
        document.getElementById('home-btn').addEventListener('click', () => {
            hideAllMenus();
            mainMenu.classList.remove('hidden');
            gameState = 'menu';
        });

        resize();
    </script>
</body>
</html>
"""

st.title("🎮 Neon Bounce")
st.caption("Streamlit에서 실행되는 네온 액션 플랫포머 게임입니다. [A/D] 이동 | [Shift/X] 대쉬")

# Streamlit Component로 HTML 렌더링
components.html(HTML_CODE, height=720, scrolling=False)
