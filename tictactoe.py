import pygame
import sys
import math
import random
import time
 
# --- (1) CẤU HÌNH & KHỞI TẠO CƠ BẢN ---
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Tic-Tac-Toe")
 
# --- HẰNG SỐ GAME ---
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
AI_PLAYER = PLAYER_O
HUMAN_PLAYER = PLAYER_X
 
# --- QUẢN LÝ MÀU SẮC (THEME) ---
THEME_LIGHT = {
    'BG': (28, 170, 156), 'GRID': (13, 161, 146), 'X': (84, 84, 84), 'O': (242, 235, 211),
    'TEXT': (255, 255, 255), 'BUTTON': (60, 60, 60), 'BUTTON_HOVER': (100, 100, 100),
    'MODAL_BG': (240, 240, 240), 'MODAL_BORDER': (60, 60, 60), 'MODAL_TEXT': (0, 0, 0)
}
 
THEME_DARK = {
    'BG': (60, 60, 60), 'GRID': (100, 100, 100), 'X': (255, 100, 100), 'O': (100, 200, 255),
    'TEXT': (240, 240, 240), 'BUTTON': (40, 40, 40), 'BUTTON_HOVER': (70, 70, 70),
    'MODAL_BG': (50, 50, 50), 'MODAL_BORDER': (200, 200, 200), 'MODAL_TEXT': (255, 255, 255)
}
 
# Biến toàn cục (Global State)
current_theme = THEME_LIGHT
is_dark_mode = False
is_music_on = True
 
def apply_theme():
    """Áp dụng bộ màu hiện tại cho các biến toàn cục."""
    global COLOR_BG, COLOR_GRID, COLOR_X, COLOR_O, COLOR_TEXT, COLOR_BUTTON, COLOR_BUTTON_HOVER
    global COLOR_MODAL_BG, COLOR_MODAL_BORDER, COLOR_MODAL_TEXT
   
    COLOR_BG = current_theme['BG']
    COLOR_GRID = current_theme['GRID']
    COLOR_X = current_theme['X']
    COLOR_O = current_theme['O']
    COLOR_TEXT = current_theme['TEXT']
    COLOR_BUTTON = current_theme['BUTTON']
    COLOR_BUTTON_HOVER = current_theme['BUTTON_HOVER']
    COLOR_MODAL_BG = current_theme['MODAL_BG']
    COLOR_MODAL_BORDER = current_theme['MODAL_BORDER']
    COLOR_MODAL_TEXT = current_theme['MODAL_TEXT']
 
def toggle_theme():
    """Chuyển đổi giữa Dark và Light mode."""
    global is_dark_mode, current_theme
    is_dark_mode = not is_dark_mode
    current_theme = THEME_DARK if is_dark_mode else THEME_LIGHT
    apply_theme()
 
apply_theme()
 
# --- FONT ---
try: FONT_GEAR = pygame.font.SysFont('Segoe UI Symbol', 40)
except: FONT_GEAR = pygame.font.SysFont('Arial', 40)
FONT_LARGE = pygame.font.SysFont('Arial', 40, bold=True)
FONT_MEDIUM = pygame.font.SysFont('Arial', 28, bold=True)
FONT_SMALL = pygame.font.SysFont('Arial', 20, bold=True)
 
# --- MUSIC ---
try:
    pygame.mixer.music.load('Grow a Garden Soundtrack - Main Theme 2.mp3')
    pygame.mixer.music.set_volume(0.5)
except:
    pass
def start_music():
    if is_music_on and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
def stop_music(): pygame.mixer.music.stop()
def toggle_music():
    global is_music_on
    is_music_on = not is_music_on
    if is_music_on: start_music()
    else: stop_music()
 
# --- (2) LOGIC GAME CHUNG ---
def create_board(board_size): return [[EMPTY for _ in range(board_size)] for _ in range(board_size)]
def get_valid_moves(board):
    moves = []
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == EMPTY: moves.append((r, c))
    return moves
def is_board_full(board): return len(get_valid_moves(board)) == 0
def make_move(board, move, player):
    row, col = move
    if board[row][col] == EMPTY: board[row][col] = player; return True
    return False
def undo_move(board, move): board[move[0]][move[1]] = EMPTY
def check_win(board, player, board_size, win_length):
    # Ngang
    for r in range(board_size):
        for c in range(board_size - win_length + 1):
            if all(board[r][c + i] == player for i in range(win_length)): return True
    # Dọc
    for c in range(board_size):
        for r in range(board_size - win_length + 1):
            if all(board[r + i][c] == player for i in range(win_length)): return True
    # Chéo \
    for r in range(board_size - win_length + 1):
        for c in range(board_size - win_length + 1):
            if all(board[r + i][c + i] == player for i in range(win_length)): return True
    # Chéo /
    for r in range(win_length - 1, board_size):
        for c in range(board_size - win_length + 1):
            if all(board[r - i][c + i] == player for i in range(win_length)): return True
    return False
 
# --- (3) AI MINIMAX BẤT BẠI (Chỉ 3x3) ---
def minimax_3x3(board, is_maximizing):
    if check_win(board, AI_PLAYER, 3, 3): return 1
    if check_win(board, HUMAN_PLAYER, 3, 3): return -1
    if is_board_full(board): return 0
    if is_maximizing:
        best = -math.inf
        for move in get_valid_moves(board):
            make_move(board, move, AI_PLAYER); score = minimax_3x3(board, False); undo_move(board, move)
            best = max(score, best)
        return best
    else:
        best = math.inf
        for move in get_valid_moves(board):
            make_move(board, move, HUMAN_PLAYER); score = minimax_3x3(board, True); undo_move(board, move)
            best = min(score, best)
        return best
def find_best_move_3x3(board):
    best_score = -math.inf; best_move = None
    for move in get_valid_moves(board):
        make_move(board, move, AI_PLAYER); score = minimax_3x3(board, False); undo_move(board, move)
        if score > best_score: best_score = score; best_move = move
    return best_move
 
# --- (4) HÀM VẼ VÀ GIAO DIỆN CHUNG ---
def draw_text(screen, text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center: text_rect.center = (x, y)
    else: text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
 
def draw_button(screen, rect, text, mouse_pos, font=FONT_MEDIUM, bg_color=None, text_color=None):
    if bg_color is None: bg_color = COLOR_BUTTON
    if text_color is None: text_color = COLOR_TEXT
    final_color = bg_color
    if rect.collidepoint(mouse_pos): final_color = COLOR_BUTTON_HOVER
   
    pygame.draw.rect(screen, final_color, rect, border_radius=10)
    pygame.draw.rect(screen, COLOR_TEXT, rect, width=2, border_radius=10)
    draw_text(screen, text, font, text_color, rect.centerx, rect.centery)
 
def open_settings_modal(screen, in_game=False):
    """Mở bảng cài đặt."""
   
    original_screen = screen.copy()
   
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))
   
    w, h = screen.get_size()
    modal_w, modal_h = 400, 350
    modal_rect = pygame.Rect((w - modal_w)//2, (h - modal_h)//2, modal_w, modal_h)
   
    btn_theme = pygame.Rect(modal_rect.centerx - 120, modal_rect.top + 80, 240, 50)
    btn_music = pygame.Rect(modal_rect.centerx - 120, modal_rect.top + 150, 240, 50)
   
    if in_game:
        btn_return = pygame.Rect(modal_rect.centerx - 120, modal_rect.top + 220, 240, 50)
        btn_close = pygame.Rect(modal_rect.centerx - 120, modal_rect.top + 285, 240, 50)
    else:
        btn_return = None
        btn_close = pygame.Rect(modal_rect.centerx - 120, modal_rect.top + 220, 240, 50)
   
    running = True
    while running:
        pygame.draw.rect(screen, COLOR_MODAL_BG, modal_rect, border_radius=15)
        pygame.draw.rect(screen, COLOR_MODAL_BORDER, modal_rect, width=3, border_radius=15)
       
        draw_text(screen, "SETTINGS", FONT_LARGE, COLOR_MODAL_TEXT, modal_rect.centerx, modal_rect.top + 40)
       
        mouse_pos = pygame.mouse.get_pos()
       
        txt_theme = "Theme: Dark (Gray)" if is_dark_mode else "Theme: Light (Cyan)"
        txt_music = "Music: ON" if is_music_on else "Music: MUTE"
       
        draw_button(screen, btn_theme, txt_theme, mouse_pos, text_color=COLOR_MODAL_TEXT)
        draw_button(screen, btn_music, txt_music, mouse_pos, text_color=COLOR_MODAL_TEXT)
        draw_button(screen, btn_close, "Close Settings", mouse_pos, text_color=COLOR_MODAL_TEXT)
        if btn_return:
            draw_button(screen, btn_return, "Quit Match", mouse_pos, text_color=COLOR_MODAL_TEXT)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_theme.collidepoint(mouse_pos):
                    toggle_theme()
                    screen.blit(original_screen, (0,0))
                    screen.blit(overlay, (0,0))
                elif btn_music.collidepoint(mouse_pos): toggle_music()
                elif btn_close.collidepoint(mouse_pos): running = False
                elif btn_return and btn_return.collidepoint(mouse_pos): return "quit_game"
       
        pygame.display.update()
    return "continue"
 
def draw_grid_centered(screen, board_size, square_size, start_x, start_y):
    """Vẽ lưới dựa trên toạ độ start_x, start_y để đảm bảo ở giữa."""
    screen.fill(COLOR_BG)
    grid_w = board_size * square_size
    grid_h = board_size * square_size
   
    # Vẽ các đường
    for i in range(0, board_size + 1):
        # Dọc
        pygame.draw.line(screen, COLOR_GRID,
                         (start_x + i*square_size, start_y),
                         (start_x + i*square_size, start_y + grid_h), 4)
        # Ngang
        pygame.draw.line(screen, COLOR_GRID,
                         (start_x, start_y + i*square_size),
                         (start_x + grid_w, start_y + i*square_size), 4)
 
def draw_pieces_centered(screen, board, board_size, square_size, start_x, start_y):
    """Vẽ X và O căn giữa."""
    radius = int(square_size * 0.35)
    width = int(square_size * 0.1)
   
    for r in range(board_size):
        for c in range(board_size):
            cx = start_x + c*square_size + square_size//2
            cy = start_y + r*square_size + square_size//2
           
            if board[r][c] == PLAYER_X:
                pygame.draw.line(screen, COLOR_X, (cx-radius, cy-radius), (cx+radius, cy+radius), width)
                pygame.draw.line(screen, COLOR_X, (cx+radius, cy-radius), (cx-radius, cy+radius), width)
            elif board[r][c] == PLAYER_O:
                pygame.draw.circle(screen, COLOR_O, (cx, cy), radius, width)
 
def get_clicked_pos_centered(pos, board_size, square_size, start_x, start_y):
    """Lấy (hàng, cột) từ vị trí click chuột (dùng cho chế độ căn giữa)."""
    x, y = pos
    grid_w = board_size * square_size
    grid_h = board_size * square_size
   
    if x < start_x or x > start_x + grid_w or y < start_y or y > start_y + grid_h:
        return None
   
    col = (x - start_x) // square_size
    row = (y - start_y) // square_size
    return (row, col)
 
# --- (5) VÒNG LẶP GAME CHÍNH (DYNAMIC RESIZE & CĂN GIỮA) ---
def play_game_loop(board_size, win_length, is_ai_game, ai_starts=False):
   
    # 1. Khởi tạo kích thước cửa sổ tối thiểu và cờ RESIZABLE
    MIN_SIZE = 600
    window_width = MIN_SIZE
    window_height = MIN_SIZE + 100
   
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption(f"Tic-Tac-Toe {board_size}x{board_size} (Win {win_length})")
   
    # Cấu hình game ban đầu
    board = create_board(board_size)
    game_over = False
   
    if is_ai_game and ai_starts:
        current_player = AI_PLAYER; message = "AI's Turn (O)"
        initial_move = (random.randint(0, board_size-1), random.randint(0, board_size-1))
        make_move(board, initial_move, AI_PLAYER)
        current_player = HUMAN_PLAYER
        message = "Your Turn (X)"
    else:
        current_player = HUMAN_PLAYER; message = f"Player {current_player}'s Turn"
 
    running = True
    while running:
       
        # 2. Tái tính toán kích thước bàn cờ và căn giữa theo cửa sổ hiện tại
        window_width, window_height = screen.get_size()
        info_h = 100 # Vùng thông báo cố định ở dưới
        margin = 40
       
        max_board_w = window_width - 2 * margin
        max_board_h = window_height - info_h - 2 * margin
       
        square_size = min(max_board_w // board_size, max_board_h // board_size)
        square_size = max(square_size, 20)
       
        board_pixel_w = board_size * square_size
        board_pixel_h = board_size * square_size
       
        start_x = (window_width - board_pixel_w) // 2
        start_y = (window_height - info_h - board_pixel_h) // 2
       
        btn_settings = pygame.Rect(window_width - 60, 10, 50, 50)
        msg_y = window_height - info_h // 2
       
        # Lấy vị trí chuột (KHẮC PHỤC LỖI NAMEERROR)
        mouse_pos = pygame.mouse.get_pos()
 
        # 3. Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
           
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_settings.collidepoint(mouse_pos):
                    if open_settings_modal(screen, in_game=True) == "quit_game": return
               
                if not game_over and (current_player == HUMAN_PLAYER or not is_ai_game):
                    move = get_clicked_pos_centered(mouse_pos, board_size, square_size, start_x, start_y)
                   
                    if move and board[move[0]][move[1]] == EMPTY:
                        make_move(board, move, current_player)
                       
                        if check_win(board, current_player, board_size, win_length):
                            game_over = True; message = f"Player {current_player} WINS!"
                        elif is_board_full(board):
                            game_over = True; message = "It's a DRAW!"
                        else:
                            current_player = AI_PLAYER if is_ai_game else (PLAYER_O if current_player == PLAYER_X else PLAYER_X)
                            message = "AI is thinking..." if is_ai_game else f"Player {current_player}'s Turn"
       
        # 4. Lượt của AI
        if is_ai_game and current_player == AI_PLAYER and not game_over:
            # Vẽ trạng thái "AI Thinking" trước
            draw_grid_centered(screen, board_size, square_size, start_x, start_y)
            draw_pieces_centered(screen, board, board_size, square_size, start_x, start_y)
            draw_text(screen, message, FONT_MEDIUM, COLOR_TEXT, window_width//2, msg_y)
            pygame.display.update()
           
            if board_size == 3: ai_move = find_best_move_3x3(board)
            else:
                valid_moves = get_valid_moves(board)
                ai_move = random.choice(valid_moves) if valid_moves else None
           
            if ai_move:
                make_move(board, ai_move, AI_PLAYER)
                if check_win(board, AI_PLAYER, board_size, win_length):
                    game_over = True; message = "AI WINS!"
                elif is_board_full(board):
                    game_over = True; message = "It's a DRAW!"
                else:
                    current_player = HUMAN_PLAYER; message = "Your Turn (X)"
 
        # 5. Vẽ lại tất cả
        draw_grid_centered(screen, board_size, square_size, start_x, start_y)
        draw_pieces_centered(screen, board, board_size, square_size, start_x, start_y)
       
        color_gear = COLOR_BUTTON_HOVER if btn_settings.collidepoint(mouse_pos) else COLOR_BUTTON
        draw_text(screen, "\u2699", FONT_GEAR, color_gear, btn_settings.centerx, btn_settings.centery)
        draw_text(screen, message, FONT_MEDIUM, COLOR_TEXT, window_width//2, msg_y)
 
        pygame.display.update()
 
        # 6. Xử lý kết thúc game
        if game_over:
            pygame.time.wait(2000) # Đợi 2 giây
            running = False
 
# --- (6) CÁC MENU ĐIỀU HƯỚNG ---
MENU_WIDTH = 500
MENU_HEIGHT = 600
 
def main_menu():
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe Menu")
    start_music()
   
    center_x = MENU_WIDTH // 2
    start_y = 180
    gap = 70
   
    btn_pvp = pygame.Rect(center_x - 150, start_y, 300, 50)
    btn_pve = pygame.Rect(center_x - 150, start_y + gap, 300, 50)
    btn_custom = pygame.Rect(center_x - 150, start_y + gap*2, 300, 50)
    btn_quit = pygame.Rect(center_x - 150, start_y + gap*3, 300, 50)
   
    btn_settings = pygame.Rect(MENU_WIDTH - 60, 10, 50, 50)
   
    while True:
        screen.fill(COLOR_BG)
        draw_text(screen, "TIC-TAC-TOE", FONT_LARGE, COLOR_TEXT, center_x, 80)
        draw_text(screen, "MENU", FONT_MEDIUM, COLOR_TEXT, center_x, 120)
       
        mouse_pos = pygame.mouse.get_pos()
       
        draw_button(screen, btn_pvp, "Standard PvP", mouse_pos)
        draw_button(screen, btn_pve, "Player vs AI (3x3)", mouse_pos)
        draw_button(screen, btn_custom, "Custom Match (PvP)", mouse_pos)
        draw_button(screen, btn_quit, "Exit", mouse_pos)
       
        color_gear = COLOR_BUTTON_HOVER if btn_settings.collidepoint(mouse_pos) else COLOR_BUTTON
        draw_text(screen, "\u2699", FONT_GEAR, color_gear, btn_settings.centerx, btn_settings.centery)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pvp.collidepoint(mouse_pos):
                    pvp_menu()
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                elif btn_pve.collidepoint(mouse_pos):
                    pve_menu()
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                elif btn_custom.collidepoint(mouse_pos):
                    custom_game_menu()
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                elif btn_quit.collidepoint(mouse_pos):
                    stop_music(); pygame.quit(); sys.exit()
                elif btn_settings.collidepoint(mouse_pos):
                    open_settings_modal(screen, in_game=False)
                   
        pygame.display.update()
 
def pvp_menu():
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("PvP Menu - Select Format")
    btn_3 = pygame.Rect(100, 180, 300, 50)
    btn_5 = pygame.Rect(100, 250, 300, 50)
    btn_7 = pygame.Rect(100, 320, 300, 50)
    btn_back = pygame.Rect(100, 450, 300, 50)
    while True:
        screen.fill(COLOR_BG)
        draw_text(screen, "STANDARD SIZES (PvP)", FONT_LARGE, COLOR_TEXT, MENU_WIDTH//2, 80)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, btn_3, "3x3 (Win 3)", mouse_pos)
        draw_button(screen, btn_5, "5x5 (Win 4)", mouse_pos)
        draw_button(screen, btn_7, "7x7 (Win 5)", mouse_pos)
        draw_button(screen, btn_back, "Back", mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_3.collidepoint(mouse_pos): play_game_loop(3,3,False); return
                elif btn_5.collidepoint(mouse_pos): play_game_loop(5,4,False); return
                elif btn_7.collidepoint(mouse_pos): play_game_loop(7,5,False); return
                elif btn_back.collidepoint(mouse_pos): return
        pygame.display.update()
 
def pve_menu():
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("PvE Menu - Select Side")
    btn_x = pygame.Rect(100, 180, 300, 50); btn_o = pygame.Rect(100, 250, 300, 50); btn_back = pygame.Rect(100, 350, 300, 50)
    while True:
        screen.fill(COLOR_BG)
        draw_text(screen, "PLAYER VS AI (3x3)", FONT_LARGE, COLOR_TEXT, MENU_WIDTH//2, 80)
        draw_text(screen, "(Unbeatable AI)", FONT_MEDIUM, COLOR_TEXT, MENU_WIDTH//2, 120)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, btn_x, "Play as X (Go First)", mouse_pos); draw_button(screen, btn_o, "Play as O (Go Second)", mouse_pos); draw_button(screen, btn_back, "Back", mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_x.collidepoint(mouse_pos): play_game_loop(3,3,True,False); return
                elif btn_o.collidepoint(mouse_pos): play_game_loop(3,3,True,True); return
                elif btn_back.collidepoint(mouse_pos): return
        pygame.display.update()
 
def custom_game_menu():
    MENU_W, MENU_H = 500, 600
    screen = pygame.display.set_mode((MENU_W, MENU_H))
    pygame.display.set_caption("Custom Match - PvP")
   
    c_size = 10
    c_win = 5
   
    btn_start = pygame.Rect(100, 480, 300, 60)
    btn_back = pygame.Rect(100, 550, 300, 40)
    btn_size_dec = pygame.Rect(100, 200, 60, 60); btn_size_inc = pygame.Rect(340, 200, 60, 60)
    btn_win_dec = pygame.Rect(100, 350, 60, 60); btn_win_inc = pygame.Rect(340, 350, 60, 60)
   
    while True:
        screen.fill(COLOR_BG)
        draw_text(screen, "CUSTOM MATCH (PvP)", FONT_LARGE, COLOR_TEXT, MENU_W//2, 80)
       
        mouse_pos = pygame.mouse.get_pos()
       
        draw_text(screen, "Board Size (3-20)", FONT_MEDIUM, COLOR_TEXT, 250, 160)
        draw_button(screen, btn_size_dec, "-", mouse_pos, FONT_LARGE)
        draw_button(screen, btn_size_inc, "+", mouse_pos, FONT_LARGE)
        draw_text(screen, f"{c_size} x {c_size}", FONT_LARGE, COLOR_TEXT, 250, 230)
       
        draw_text(screen, "Win Condition (3-Size)", FONT_MEDIUM, COLOR_TEXT, 250, 310)
        draw_button(screen, btn_win_dec, "-", mouse_pos, FONT_LARGE)
        draw_button(screen, btn_win_inc, "+", mouse_pos, FONT_LARGE)
        draw_text(screen, f"Connect {c_win}", FONT_LARGE, COLOR_TEXT, 250, 380)
       
        draw_button(screen, btn_start, "START GAME", mouse_pos)
        draw_button(screen, btn_back, "Back", mouse_pos, FONT_SMALL)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(mouse_pos): return
               
                if btn_size_dec.collidepoint(mouse_pos) and c_size > 3: c_size -= 1
                if btn_size_inc.collidepoint(mouse_pos) and c_size < 20: c_size += 1
               
                c_win = min(c_win, c_size)
                if btn_win_dec.collidepoint(mouse_pos) and c_win > 3: c_win -= 1
                if btn_win_inc.collidepoint(mouse_pos) and c_win < c_size: c_win += 1
               
                if btn_start.collidepoint(mouse_pos):
                    play_game_loop(c_size, c_win, is_ai_game=False)
                    screen = pygame.display.set_mode((MENU_W, MENU_H))
       
        pygame.display.update()
 
# --- (7) BẮT ĐẦU TRÒ CHƠI ---
if __name__ == "__main__":
    main_menu()
 