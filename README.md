# flappybird
import pygame
import random
import os

# Oyun ayarları
WIDTH, HEIGHT = 400, 600
gravity = 0.6
flap_strength =- 10
pipe_gap = 180  # Borular arasındaki boşluğu artırdık
pipe_width = 70
pipe_speed = 3 

# Renkler
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)  # Açık yeşil
DARK_GREEN = (0, 128, 0)  # Koyu yeşil

pygame.init()

# Ekranı oluştur
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        # Dosya yolunu burada tam olarak belirtiyoruz
        BIRD_IMAGE_PATH = r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\bird.png"
        
        # Dosyanın gerçekten mevcut olup olmadığını kontrol edelim
        if os.path.exists(BIRD_IMAGE_PATH):
            self.image = pygame.image.load(BIRD_IMAGE_PATH)  # Burada dosyayı yüklüyoruz
            self.image = pygame.transform.scale(self.image, (50, 35))  # Boyutlandır
        else:
            raise FileNotFoundError(f"{BIRD_IMAGE_PATH} dosyası bulunamadı!")

        # Kuşun boyutlarını belirliyoruz (Yükseklik ve Genişlik)
        self.width = 50
        self.height = 35

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

    def flap(self):
        self.velocity = flap_strength

    def draw(self):
        screen.blit(self.image, (self.x, int(self.y)))  # Kuşu ekrana çiz

class Pipe:
    def __init__(self, x):
        self.x = x
        # Boru yüksekliğini daha farklı bir şekilde rastgele seçiyoruz
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)

    def update(self):
        self.x -= pipe_speed

    def draw(self):
        # Boruların şekillerini daha estetik yapmak için border_radius ekliyoruz
        pygame.draw.rect(screen, LIGHT_GREEN, (self.x, 0, pipe_width, self.height), border_radius=15)
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.height + pipe_gap, pipe_width, HEIGHT - (self.height + pipe_gap)), border_radius=15)

# Başlangıç ayarları
bird = Bird()
pipes = [Pipe(WIDTH + i * 250) for i in range(3)]  # Borular arasında daha fazla mesafe bıraktık
score = 0
high_score = 0
running = True

while running:
    screen.fill(WHITE)

    # Olayları al
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()

    bird.update()
    bird.draw()

    for pipe in pipes:
        pipe.update()
        pipe.draw()
        if pipe.x + pipe_width < 0:
            pipes.remove(pipe)
            pipes.append(Pipe(WIDTH))
            score += 1

        # Çarpma kontrolü: sadece boruya fiziksel olarak çarpınca game over olacak
        if (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe_width):  # Kuşun x koordinatını doğru kontrol et
            # Çarpma için daha esnek bir alan ekliyoruz, borunun alt kısmı ile üst kısmı arasında geçişi sağlıyoruz
            if bird.y < pipe.height or bird.y + bird.height > pipe.height + pipe_gap:  # Boruya çarpma kontrolü
                print("Çarpma gerçekleşti!")
                running = False

    # Kuşun ekran dışında kalmasını kontrol et
    if bird.y + bird.height > HEIGHT or bird.y < 0:
        print("Yere düştü veya yukarıya çarptı!")
        running = False

    # Skoru ekrana yazdır
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 30))  # Merkezde göstermek için
    screen.blit(score_text, score_rect)

    # High score ekrana yazdır
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, 60))
    screen.blit(high_score_text, high_score_rect)

    # Oyun bitince mesaj göster
    if not running:
        if score > high_score:  # Eğer yeni skor yüksekse, high score'u güncelle
            high_score = score
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (0, 0, 0))
        quit_text = font.render("Press Q to Quit", True, (0, 0, 0))

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Oyun sonu tuş kontrolü
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q tuşuna basıldığında çık
                        waiting_for_input = False
                    elif event.key == pygame.K_r:  # R tuşuna basıldığında oyunu yeniden başlat
                        bird = Bird()
                        pipes = [Pipe(WIDTH + i * 250) for i in range(3)]
                        score = 0
                        running = True
                        waiting_for_input = False

            # Kullanıcı herhangi bir tuşa basmadıysa ekranı güncellemeye devam et
            pygame.display.flip()
            clock.tick(30)  # Bu satır yerine daha az bekleme ekledik

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
