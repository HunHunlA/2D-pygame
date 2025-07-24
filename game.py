import pygame, sys
import random
from button import Button

def game_over_screen(score):
    screen.fill((0, 0, 0))  # Đổ màu đen cho màn hình
    game_over_text = game_font.render(f"Game Over - Your Score: {score}", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting_for_key = False
                main_menu()
    
def game_win_screen(score):
    screen.fill((255, 255, 255))  # Đặt màu nền là đen

    win_text = game_font.render(f"You life - Your Score: {score}", True, (255, 0, 0))
    win_rect = win_text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(win_text, win_rect) 
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting_for_key = False
                main_menu()
    
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)

class Bird():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.speed = [random.randint(2, 4), random.randint(2, 4)]
        self.visible = True  # Thêm trạng thái visible cho chim
        self.hit_effect_image = pygame.image.load('image/ban_trung.png').convert_alpha()
        self.hit_effect_image = pygame.transform.scale(self.hit_effect_image, (220, 110))
        self.hit_effect_duration = 100
        self.hit_effect_visible = False  # Trạng thái hiển thị hiệu ứng
        self.hit_effect_time = 0  # Thời điểm hiệu ứng được kích hoạt
        
    def update(self):
        if self.visible:  # Cập nhật chỉ khi chim là visible
            self.rect.move_ip(self.speed)
            # Kiểm tra và điều chỉnh nếu con chim gần biên màn hình
            
            margin = 100  # Khoảng cách từ biên màn hình để kích thích quay lại
            if self.rect.left < margin:
                self.rect.left = margin
                self.speed[0] = -self.speed[0]
            elif self.rect.right > width - margin:
                self.rect.right = width - margin
                self.speed[0] = -self.speed[0]
            if self.rect.top < margin:
                self.rect.top = margin
                self.speed[1] = -self.speed[1]
            elif self.rect.bottom > height - margin:
                self.rect.bottom = height - margin
                self.speed[1] = -self.speed[1]

    def show_hit_effect(self, screen):
        if self.visible and pygame.time.get_ticks() - self.hit_effect_time < self.hit_effect_duration:
            screen.blit(self.hit_effect_image, self.rect)

pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)
pygame.mixer.init()

SCREEN = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Menu")
BG = pygame.image.load("image/main_menu.jpg")
screen = pygame.display.set_mode((1200, 700))
game_over = False
game_win = False

size = 1200, 700
width, height = size
clock = pygame.time.Clock()

bg = pygame.image.load('image/rungsau.jpg').convert_alpha()
bg = pygame.transform.scale(bg, size)

bird_image = pygame.image.load('image/chim1.png').convert_alpha()
bird_image = pygame.transform.scale(bird_image, (220, 110))

boss_image = pygame.image.load('image/bos.png').convert_alpha()
boss_image = pygame.transform.scale(boss_image, (300,150))

gun = pygame.image.load('image/gun.png').convert_alpha()
gun = pygame.transform.scale(gun, (380, 180))

tam = pygame.image.load('image/tam.png').convert_alpha()
tam = pygame.transform.scale(tam, (25, 25))
tam_rect = tam.get_rect(center=(600, 350))

no = pygame.image.load('image/no.png').convert_alpha()
no = pygame.transform.scale(no, (500, 500))
no_rect = no.get_rect(center = (600, 350))

hop = pygame.image.load('image/hop.png').convert_alpha()
hop = pygame.transform.scale(hop, (90, 90))
box_rect = hop.get_rect(x=random.randint(0, width - 200), y=-200)  # Khởi tạo hộp nằm ngoài màn hình
# Thêm biến để theo dõi thời gian giữa các lần hiển thị hộp mới

score = 0

boxes = []
box_visible = False

def play():
    game_over = False
    game_win = False

    time_between_boxes = 10000  # Đợi giây giữa các lần hiển thị hộp mới
    last_box_time = pygame.time.get_ticks()

    score = 0
    hp_width = 300
    countdown_start_time = pygame.time.get_ticks()
    countdown_duration = 4
    hp_loss = 100
    tam_speed = 5
    move_left = move_right = move_up = move_down = False
    time_between_birds = 1000
    last_bird_time = pygame.time.get_ticks()
    birds = [Bird(bird_image, random.randint(0, width), random.randint(0, height)) for _ in range(5)]

    # Thêm biến để theo dõi thời gian trôi qua từ khi bắt đầu chương trình
    elapsed_time_since_start = 0
    explosion_visible = False
    explosion_start_time = 0
    
    # Thêm các biến cho hình nền
    background_change_score1 = 20  # Điểm số cần đạt để thay đổi hình nền
    background_change_score2 = 40
    background_change_score3 = 60
    current_background_index = 0  # Chỉ số của hình nền hiện tại
    background1 = [
        pygame.image.load("image/rungsau.jpg").convert_alpha(),
    ]
    background2 = [
        pygame.image.load("image/dongco.jpg").convert_alpha(),
    ]
    background3 = [
        pygame.image.load("image/thanhpho.jpg").convert_alpha(),
    ]
    background4 = [
        pygame.image.load("image/phaodai.png").convert_alpha(),
    ]
    background1 = [pygame.transform.scale(bg, (1200, 700)) for bg in background1]
    background2 = [pygame.transform.scale(bg, (1200, 700)) for bg in background2]
    background3 = [pygame.transform.scale(bg, (1200, 700)) for bg in background3]
    background4 = [pygame.transform.scale(bg, (1200, 700)) for bg in background4]

    def change_background2():
        nonlocal current_background_index
        current_background_index = min(current_background_index + 1, len(background2) - 1)      
    def change_background3():
        nonlocal current_background_index
        current_background_index = min(current_background_index + 1, len(background3) - 1)  
    def change_background4():
        nonlocal current_background_index
        current_background_index = min(current_background_index + 1, len(background4) - 1)  

    def score_display():
        score_game = game_font.render(str(score), True, (255, 0, 0))
        scoreg_rect = score_game.get_rect(center=(1050, 50))
        screen.blit(score_game, scoreg_rect)

    def score_text():
        score_t = game_font.render('Score:', True, (255, 0, 0))
        scoret_rect = score_t.get_rect(center=(930, 50))
        screen.blit(score_t, scoret_rect)

    def hp_text():
        hp_t = game_font.render('HP', True, (0, 255, 0))
        hp_rect = hp_t.get_rect(center=(50, 665))
        screen.blit(hp_t, hp_rect)

    def hp():
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(100, 650, 300, 30))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(100, 650, hp_width, 30))

    def countdown_display():
        countdown_text = game_font.render(f"Time: {remaining_time}", True, (255, 255, 255))
        countdown_rect = countdown_text.get_rect(center=(600, 50))
        screen.blit(countdown_text, countdown_rect)
    
    def show_box_effect(screen, box_rect):
        box_visible = True
        box_speed = 5

        # Kiểm tra xem hộp có nên hiển thị hay không
        if box_visible:
            box_rect.y += box_speed

            # Kiểm tra va chạm với hộp
            if tam_rect.colliderect(box_rect):
                box_visible = False  # Ẩn hộp khi bắn trúng
                # Thực hiện các hành động khác khi bắn trúng hộp

            # Kiểm tra nếu hộp chạm đến đáy màn hình
            if box_rect.y > height:
                boxes.remove(box_rect)  # Loại bỏ hộp khỏi danh sách
                box_visible = False

            # Hiển thị hộp
            screen.blit(pygame.transform.scale(hop, (90, 90)), box_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_UP:
                    move_up = True
                elif event.key == pygame.K_DOWN:
                    move_down = True
                if event.key == pygame.K_a:
                    for bird in birds:
                        if bird.rect.colliderect(tam_rect) and bird.visible:
                            # Khi bắn trúng chim, tăng thêm 3 giây vào thời gian đếm ngược
                            current_time = pygame.time.get_ticks()
                            remaining_time = max(0, countdown_duration - (current_time - countdown_start_time) // 1000)
                            remaining_time += 1  # Cộng thêm 3 giây vào thời gian còn lại
                            countdown_duration = remaining_time  # Cập nhật lại countdown_duration
                            countdown_start_time = current_time
                            bird.visible = False
                            bird.hit_effect_visible = True
                            bird.hit_effect_time = pygame.time.get_ticks()
                            score += 1  # Tăng điểm số khi bắn trúng chim

                    for box_rect in boxes:
                        if tam_rect.colliderect(box_rect):
                            box_visible = False
                            boxes.remove(box_rect)
                            
                            # Sự kiện ngẫu nhiên khi bắn trúng hộp
                            event = random.choice(["heal", "explosion"])

                            if event == "heal":
                                hp_width = min(300, hp_width + 30)  # Hồi thêm 30 máu, giới hạn tối đa là 300
                            elif event == "explosion":
                                remaining_time = max(0, countdown_duration - (current_time - countdown_start_time) // 1000)
                                remaining_time += 5  # Cộng thêm 3 giây vào thời gian còn lại
                                countdown_duration = remaining_time  # Cập nhật lại countdown_duration
                                countdown_start_time = current_time
                                score += 5
                                for bird in birds:
                                    bird.visible = False 
                                explosion_visible = True
                                explosion_start_time = pygame.time.get_ticks()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_UP:
                    move_up = False
                elif event.key == pygame.K_DOWN:
                    move_down = False
                    
        if move_left and tam_rect.left > 0:
            tam_rect.x -= tam_speed
        if move_right and tam_rect.right < width:
            tam_rect.x += tam_speed
        if move_up and tam_rect.top > 0:
            tam_rect.y -= tam_speed
        if move_down and tam_rect.bottom < height:
            tam_rect.y += tam_speed

        elapsed_time = (pygame.time.get_ticks() - countdown_start_time) // 1000
        remaining_time = max(0, countdown_duration - elapsed_time)

        current_bird_time = pygame.time.get_ticks()

        if current_bird_time - last_bird_time > time_between_birds and len(birds):
            last_bird_time = current_bird_time
            new_bird = Bird(bird_image, random.randint(0, width), random.randint(0, height))
            birds.append(new_bird)

        for bird in birds:
            bird.update()

        if remaining_time == 0 and score < 20:
            hp_width = max(0, hp_width - hp_loss)
            countdown_duration = 3
            countdown_start_time = pygame.time.get_ticks()
        
        screen.blit(bg, (0, 0))
        if score >= background_change_score1:
            change_background2()
            screen.blit(background2[current_background_index], (0, 0))
        if score >= background_change_score2:
            change_background3()
            screen.blit(background3[current_background_index], (0, 0))
        if score >= background_change_score3:
            change_background4()
            screen.blit(background4[current_background_index], (0, 0))
        
        elapsed_time_since_start += clock.tick(120)
        
        current_time = pygame.time.get_ticks()
        if explosion_visible:
            screen.blit(no, no_rect)
            if current_time - explosion_start_time >= 1000:  # 1000 miliseconds = 1 giây
                explosion_visible = False  # Biến mất hiệu ứng "no" sau 1 giây
                
        # Hiển thị hộp sau khi đã trôi qua một khoảng thời gian
        if elapsed_time_since_start >= time_between_boxes:
            box_visible = True

            # Kiểm tra nếu đã đến lúc hiển thị hộp mới
            if current_bird_time - last_box_time > time_between_boxes:
                last_box_time = current_bird_time
                new_box_rect = pygame.Rect(random.randint(0, width - 200), -200, 100, 100)
                boxes.append(new_box_rect)

        # Hiển thị và cập nhật hộp trong danh sách
        for box_rect in boxes:
            show_box_effect(screen, box_rect)
        
        for bird in birds:
            if bird.visible:
                bird.show_hit_effect(screen)
                screen.blit(bird_image, bird.rect)
            screen.blit(tam, tam_rect)
            if bird.hit_effect_visible:
                current_time = pygame.time.get_ticks()
                if current_time - bird.hit_effect_time < bird.hit_effect_duration:
                    screen.blit(bird.hit_effect_image, bird.rect)
                else:
                    bird.hit_effect_visible = False
                    
        if hp_width <= 0:
            hp_width = 0
            game_over = True                 
        
        if remaining_time == 0 and score >= 20:
            game_win = True

        if game_over:
            game_over_screen(score)
        if game_win:
            game_win_screen(score)
            
        screen.blit(gun, (470, 520))
        score_display()
        score_text()
        hp()
        hp_text()
        countdown_display()
        
        clock.tick(120)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

            
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("nhan phim mui ten de di chuyen, phim 'a' de ban", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("image/Play Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("image/Options Rect.png"), pos=(640, 400),
                            text_input="Huong dan", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("image/Quit Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()