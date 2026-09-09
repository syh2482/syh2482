import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Bounce",
    page_icon="🎮",
    layout="centered"
)

html_code = """
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
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
            border-radius: 10px;
            max-width: 100%;
            max-height: 80vh;
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
            padding: 20px;
            font-size: 1.4rem;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.9);
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
        }
        .btn {
            background: linear-gradient(135deg, #0ea5e9, #2563eb);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.2rem;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            transition: transform 0.1s, box-shadow 0.1s;
            margin: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }
        .hidden {
            display: none !important;
        }
        #mobile-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 600px;
            padding: 20px;
            pointer-events: auto;
            margin-top: auto;
        }
        .control-group {
            display: flex;
            gap: 15px;
        }
        .control-btn {
            width: 65px;
            height: 65px;
            background: rgba(56, 189, 248, 0.2);
            border: 2px solid rgba(56, 189, 248, 0.5);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            color: rgba(255, 255, 255, 0.8);
            user-select: none;
            touch-action: manipulation;
        }
        .dash-btn {
            background: rgba(236, 72, 153, 0.25);
            border-color: rgba(236, 72, 153, 0.6);
            color: #f472b6;
        }
        @media (min-width: 768px) {
            #mobile-controls {
                display: none;
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
                <span id="dash-status" style="color: #f472b6;">Dash: READY</span>
                <span id="deaths-display">Deaths: 0</span>
            </div>
            
            <div id="mobile-controls">
                <div class="control-group">
                    <div class="control-btn" id="btn-left">◀</div>
                    <div class="control-btn" id="btn-right">▶</div>
                </div>
                <div class="control-btn dash-btn" id="btn-dash">⚡</div>
            </div>
        </div>

        <div id="main-menu" class="overlay">
            <div class="overlay-title">NEON<br>BOUNCE</div>
            <button class="btn" id="start-btn">Game Start</button>
            <p class="mt-4 text-slate-400">이동: ←, → (A/D) | 대쉬: Shift / X 키</p>
        </div>

        <div id="game-over" class="overlay hidden">
            <div class="overlay-title" style="color: #ef4444; text-shadow: 0 0 20px #ef4444;">GAME OVER</div>
            <button class="btn" id="retry-btn">Retry Stage</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Retry</p>
        </div>

        <div id="stage-clear" class="overlay hidden">
            <div class="overlay-title" style="color: #4ade80; text-shadow: 0 0 20px #4ade80;">STAGE CLEAR!</div>
            <button class="btn" id="next-btn">Next Stage</button>
            <p class="mt-4 text-slate-400">Press SPACE or Click Next</p>
        </div>
        
        <div id="all-clear" class="overlay hidden">
            <div class="overlay-title" style="color: #facc15; text-shadow: 0 0 20px #facc15;">ALL CLEAR!</div>
            <p id="final-stats" class="mb-6 text-2xl font-bold">Total Deaths: 0</p>
            <button class="btn" id="home-btn">Main Menu</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const uiStage = document.getElementById('stage-display');
        const uiDeaths = document.getElementById('deaths-display');
        const uiDash = document.getElementById('dash-status');
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
            DASH_GLOW: '#ec4899',
            BLOCK_BORDER: '#cbd5e1',
            MOVING_BLOCK: '#a855f7',
            MOVING_BORDER: '#c084fc',
            SPIKE: '#ef4444',
            GOAL: '#4ade80',
            GOAL_GLOW: '#16a34a'
        };

        let gameState = 'menu';
        let currentStage = 0;
        let deaths = 0;
        let animationId;
        
        const keys = { ArrowLeft: false, ArrowRight: false, a: false, d: false, Shift: false, x: false };
        let touchLeft = false;
        let touchRight = false;

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
                
                // 잔상 효과 (Trail)
                this.trail = [];
                
                // 대쉬 시스템
                this.dashCooldown = 0; // 쿨다운 프레임
                this.dashTimer = 0;    // 대쉬 지속 프레임
                this.isDashing = false;
                this.facingDir = 1;
            }

            reset() {
                this.x = this.startX;
                this.y = this.startY;
                this.vx = 0;
                this.vy = 0;
                this.trail = [];
                this.dashCooldown = 0;
                this.dashTimer = 0;
                this.isDashing = false;
            }

            triggerDash() {
                if (this.dashCooldown <= 0 && !this.isDashing) {
                    this.isDashing = true;
                    this.dashTimer = 10; // 10프레임 동안 대쉬
                    this.dashCooldown = 60; // 60프레임(1초) 쿨다운
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

                if (keys.Shift || keys.x) {
                    this.triggerDash();
                }

                // 대쉬 처리
                if (this.isDashing) {
                    this.vx = this.facingDir * (this.speed * 3.2);
                    this.vy = 0; // 대쉬 중 중력 무시
                    this.dashTimer--;
                    if (this.dashTimer <= 0) {
                        this.isDashing = false;
                    }
                } else {
                    this.vy += this.gravity;
                    if (this.vy > TILE_SIZE * 0.4) this.vy = TILE_SIZE * 0.4;
                }

                if (this.dashCooldown > 0) this.dashCooldown--;

                this.x += this.vx;
                this.y += this.vy;

                // 잔상 위치 기록 (최대 8개)
                this.trail.push({ x: this.x, y: this.y, isDash: this.isDashing });
                if (this.trail.length > 8) {
                    this.trail.shift();
                }

                if (this.y - this.radius > GAME_HEIGHT) die();
            }

            draw(ctx) {
                // 잔상 그리기
                for (let i = 0; i < this.trail.length; i++) {
                    let point = this.trail[i];
                    let alpha = (i + 1) / this.trail.length * 0.4;
                    let trailRadius = this.radius * (0.6 + 0.4 * ((i + 1) / this.trail.length));
                    
                    ctx.beginPath();
                    ctx.arc(point.x, point.y, trailRadius, 0, Math.PI * 2);
                    ctx.fillStyle = point.isDash ? COLORS.DASH_GLOW : COLORS.PLAYER;
                    ctx.globalAlpha = alpha;
                    ctx.fill();
                }
                ctx.globalAlpha = 1.0;

                // 공 본체 글로우
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius * 1.4, 0, Math.PI * 2);
                ctx.fillStyle = this.isDashing ? COLORS.DASH_GLOW : COLORS.PLAYER_GLOW;
                ctx.globalAlpha = 0.5;
                ctx.fill();
                ctx.globalAlpha = 1.0;

                // 공 본체
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.isDashing ? '#f472b6' : COLORS.PLAYER;
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
            GOAL: 9
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
                
                // 움직이는 발판 변수
                this.moveRange = TILE_SIZE * 3;
                this.moveSpeed = 1.5;
                this.moveDir = 1;
            }

            update() {
                if (this.type === BLOCK_TYPES.MOVING_HORIZ) {
                    this.x += this.moveSpeed * this.moveDir;
                    if (Math.abs(this.x - this.startX) >= this.moveRange) {
                        this.moveDir *= -1;
                    }
                } else if (this.type === BLOCK_TYPES.MOVING_VERT) {
                    this.y += this.moveSpeed * this.moveDir;
                    if (Math.abs(this.y - this.startY) >= this.moveRange) {
                        this.moveDir *= -1;
                    }
                }
            }

            draw(ctx) {
                if (this.type === BLOCK_TYPES.NORMAL) {
                    ctx.fillStyle = '#64748b';
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    ctx.strokeStyle = COLORS.BLOCK_BORDER;
                    ctx.lineWidth = 2;
                    ctx.strokeRect(this.x, this.y, this.width, this.height);
                } else if (this.type === BLOCK_TYPES.MOVING_HORIZ || this.type === BLOCK_TYPES.MOVING_VERT) {
                    ctx.fillStyle = COLORS.MOVING_BLOCK;
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    ctx.strokeStyle = COLORS.MOVING_BORDER;
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
            // Stage 1
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11100111001110011111","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 2
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11110001111000111111","11112221111222111111","11111111111111111111","00000000000000000000"],
            // Stage 3: Dash Practice
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800000000000000111","00000000000000000000","11110000000000001111","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 4: Moving Platform Intro
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800000000000000011","00000000000000000000","11110000600000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 5: Vertical Moving Platform
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00000000000000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000007000000000","00800000000000000000","11110000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 6: Dash + Moving Platforms
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00000000000000001111","00000000000000000000","00000000006000000000","00000000000000000000","00000000000000000000","00800060000000000000","11110000000000000000","11112222222222221111","11111111111111111111","00000000000000000000","00000000000000000000"]
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
                    const type = parseInt(layout[y][x]);
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
            
            // 업데이트
            for (let block of blocks) block.update();
            player.update();

            // UI 대쉬 쿨다운 업데이트
            if (player.dashCooldown <= 0) {
                uiDash.innerText = "Dash: READY (Shift)";
                uiDash.style.color = "#ec4899";
            } else {
                uiDash.innerText = `Dash: ${Math.ceil(player.dashCooldown / 60)}s`;
                uiDash.style.color = "#94a3b8";
            }

            let prevY = player.y - player.vy;
            let prevX = player.x - player.vx;

            // 충돌 로직
            for (let block of blocks) {
                if (rectCircleColliding(player, block)) {
                    if (block.type === BLOCK_TYPES.GOAL) {
                        clearStage();
                        return;
                    }
                    if (block.type >= 2 && block.type <= 5) {
                        die();
                        return;
                    }
                    if (block.type === BLOCK_TYPES.NORMAL || block.type === BLOCK_TYPES.MOVING_HORIZ || block.type === BLOCK_TYPES.MOVING_VERT) {
                        if (prevY + player.radius <= block.y + 8) {
                            player.y = block.y - player.radius;
                            player.vy = player.bounceForce;
                            // 움직이는 발판 관성 부여
                            if (block.type === BLOCK_TYPES.MOVING_HORIZ) {
                                player.x += block.moveSpeed * block.moveDir;
                            }
                        } else if (prevY - player.radius >= block.y + block.height - 8) {
                            player.y = block.y + block.height + player.radius;
                            player.vy = 0;
                        } else {
                            if (prevX < block.x) player.x = block.x - player.radius;
                            else if (prevX > block.x + block.width) player.x = block.x + block.width + player.radius;
                        }
                    }
                }
            }

            // 렌더링
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

        // 모바일 터치 및 대쉬 버튼 등록
        const setupMobileControl = (id, dir) => {
            const btn = document.getElementById(id);
            const start = (e) => { e.preventDefault(); if (dir === 'left') touchLeft = true; if (dir === 'right') touchRight = true; if (dir === 'dash' && player) player.triggerDash(); };
            const end = (e) => { e.preventDefault(); if (dir === 'left') touchLeft = false; if (dir === 'right') touchRight = false; };
            btn.addEventListener('touchstart', start);
            btn.addEventListener('touchend', end);
            btn.addEventListener('mousedown', start);
            btn.addEventListener('mouseup', end);
        };

        setupMobileControl('btn-left', 'left');
        setupMobileControl('btn-right', 'right');
        setupMobileControl('btn-dash', 'dash');

        document.getElementById('start-btn').addEventListener('click', startGame);
        document.getElementById('retry-btn').addEventListener('click', retryStage);
        document.getElementById('next-btn').addEventListener('click', nextStage);
        document.getElementById('home-btn').addEventListener('click', () => {
            hideAllMenus();
            mainMenu.classList.remove('hidden');
            gameState = 'menu';
        });

        resize();
        window.addEventListener('resize', resize);
    </script>
</body>
</html>
"""

st.title("⚡ Neon Bounce")
components.html(html_code, height=680, scrolling=False)
