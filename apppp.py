# ... existing code ...
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
                this.hasDashItem = false; // 일회용 대쉬 아이템 획득 여부
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
                this.hasDashItem = false;
                this.dashTimer = 0;
                this.isDashing = false;
            }

            triggerDash() {
                if (this.hasDashItem && !this.isDashing) {
                    this.isDashing = true;
                    this.dashTimer = 10; // 10프레임 동안 대쉬
                    this.hasDashItem = false; // 대쉬 사용 시 아이템 소모
                }
            }

            update() {
                let isMovingLeft = keys.ArrowLeft || keys.a || touchLeft;
# ... existing code ...
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

                this.x += this.vx;
                this.y += this.vy;

                // 잔상 위치 기록 (최대 8개)
# ... existing code ...
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
                
                // 움직이는 발판 변수
                this.moveRange = TILE_SIZE * 3;
# ... existing code ...
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
                    
                    cy += Math.sin(time) * 4; // 둥둥 떠다니는 효과

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
# ... existing code ...
        const stages = [
            // Stage 1
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11100111001110011111","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 2
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00800000000000000090","00000000000000000000","11110001111000111111","11112221111222111111","11111111111111111111","00000000000000000000"],
            // Stage 3: Dash Practice (공중에 아이템 추가)
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800a00000000000111","00000000000000000000","11110000000000001111","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 4: Moving Platform Intro
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00800000000000000011","00000000000000000000","11110000600000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 5: Vertical Moving Platform
            ["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000090","00000000000000001111","00000000000000000000","00000000000000000000","00000000000000000000","00000000007000000000","00800000000000000000","11110000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"],
            // Stage 6: Dash + Moving Platforms (공중에 대쉬 아이템 배치)
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
                    const type = parseInt(layout[y][x], 16); // 16진수 파싱으로 'a'를 10으로 변환
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
# ... existing code ...
            // 업데이트
            for (let block of blocks) block.update();
            player.update();

            // UI 대쉬 상태 업데이트
            if (player.hasDashItem) {
                uiDash.innerText = "Dash: AVAILABLE (Shift)";
                uiDash.style.color = "#ec4899";
            } else {
                uiDash.innerText = "Dash: NONE";
                uiDash.style.color = "#94a3b8";
            }

            let prevY = player.y - player.vy;
            let prevX = player.x - player.vx;

            // 충돌 로직
            for (let block of blocks) {
                if (block.type === BLOCK_TYPES.DASH_ITEM && block.isCollected) continue; // 획득한 아이템 무시

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
# ... existing code ...
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
            // 아이템 상태 초기화
            for (let block of blocks) {
                if (block.type === BLOCK_TYPES.DASH_ITEM) block.isCollected = false;
            }
            animationId = requestAnimationFrame(gameLoop);
        }

        function clearStage() {
# ... existing code ...
```

### 주요 변경 사항 요약:
1. **대쉬 아이템 추가**: 맵 데이터에서 `a` 문자를 사용해 대쉬 크리스탈을 맵에 배치할 수 있도록 파싱 방식을 수정했습니다.
2. **대쉬 시스템 개편**: `Player`의 `dashCooldown` 대신 `hasDashItem` 시스템으로 바꾸어 아이템 획득 시에만 1회 대쉬 가능하게 변경했습니다.
3. **완벽한 클리어 루트 (레벨 디자인 수정)**: 
    * 3스테이지에 벼랑 끝 대쉬 아이템 추가
    * 마지막 6스테이지에 공중 움직이는 발판 구간 중앙에 대쉬 아이템을 띄워 두어 점프 > 대쉬 > 착지를 연결할 수 있게 만들어 완벽히 클리어가 가능합니다! 
4. **UI 업데이트**: 쿨다운 시간 대신 획득 시 "Dash: AVAILABLE", 소진 시 "Dash: NONE"으로 표시됩니다.
