import pygame
import sys
import time
import random

pygame.init()

# Ekran boyutlarını al
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Pencere modunda ekranı aç (tam boyutlu, ancak pencere simgeleri korunur)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Miyeon Clicker")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (242, 75, 170)  # #f24baa rengi
GRAY = (200, 200, 200)  # Gri renk

font = pygame.font.SysFont("Arial", 25)

# Arka plan resmini yükle ve boyutunu ayarla
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Miyeon resmini yükle ve boyutunu ayarla
miyeon_image = pygame.image.load("miyeon.png")
miyeon_image = pygame.transform.scale(miyeon_image, (int(WIDTH * 0.5), HEIGHT))  # Ekran genişliğinin yarısı

miyeon_rect = miyeon_image.get_rect(topleft=(int(WIDTH * 0.25), 0))  # Ekranın ortasına yerleştir

# Noodle resmini yükle ve boyutunu ayarla
noodle_image = pygame.image.load("noodle.png")
noodle_image = pygame.transform.scale(noodle_image, (int(WIDTH * 0.1), int(WIDTH * 0.1)))  # Ekran genişliğinin %10'u

# Noodle resminin başlangıç konumu (Miyeon resminin üzerine gelmeyecek şekilde)
def get_random_position():
    while True:
        x = random.randint(0, WIDTH - noodle_image.get_width())
        y = random.randint(0, HEIGHT - noodle_image.get_height())
        noodle_rect = pygame.Rect(x, y, noodle_image.get_width(), noodle_image.get_height())
        # Noodle resmi Miyeon resminin üzerine gelmiyorsa konumu kabul et
        if not noodle_rect.colliderect(miyeon_rect):
            return x, y

noodle_rect = noodle_image.get_rect(topleft=get_random_position())

score = 0
click_power = 1

# Popularity Bar için değişkenler
popularity = 0
popularity_bar_width = int(WIDTH * 0.5)  # Barın genişliği (ekran genişliğinin yarısı)
popularity_bar_height = int(HEIGHT * 0.04)  # Barın yüksekliği (ekran yüksekliğinin %4'ü)
popularity_bar_x = int(WIDTH * 0.02)  # Barın sol kenardan uzaklığı (ekran genişliğinin %5'i)
popularity_bar_y = int(HEIGHT * 0.95)  # Barın alt kenardan uzaklığı (ekran yüksekliğinin %50'i)
points_for_popularity = 1000  # Her 1000 puan kazanıldığında popularity artar

# 2x güç ve geri sayım için değişkenler
power_active = False
power_start_time = 0
power_duration = 10  # 10 saniye

# Noodle resminin görünürlüğü ve yenilenme süresi
noodle_visible = True
noodle_hide_time = 0  # Noodle'ın gizlendiği zaman
noodle_spawn_interval = 17  # 17 saniyede bir
noodle_spawn_time = time.time()  # Noodle'ın göründüğü zaman

# Yuvarlak köşeli dikdörtgen çizme fonksiyonu
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Klavye tuşuna basıldığında
            if event.key == pygame.K_ESCAPE:  # ESC tuşuna basılırsa oyunu kapat
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sadece sol tıklama
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if miyeon_rect.collidepoint(mouse_x, mouse_y):
                    score += click_power
                    print(f"Miyeon'a tıklandı! Puan: {score}")
                    # Her 1000 puan kazanıldığında popularity artar ve bar sıfırlanır
                    if score >= points_for_popularity:
                        popularity += 1
                        score -= points_for_popularity  # Puanı sıfırla (ancak popularity artar)
                        print(f"Popularity Artışı: {popularity}")
                elif noodle_rect.collidepoint(mouse_x, mouse_y) and noodle_visible:  # Noodle'a tıklandı mı?
                    power_active = True  # 2x gücü aktif et
                    power_start_time = time.time()  # Şu anki zamanı kaydet
                    click_power = 2  # Tıklama gücünü 2x yap
                    noodle_visible = False  # Noodle'ı gizle
                    noodle_hide_time = time.time()  # Gizleme zamanını kaydet
                    print("2x Güç Aktif! Noodle gizlendi.")

    # Arka plan resmini çiz
    screen.blit(background_image, (0, 0))

    # Miyeon resmini ekrana çiz
    screen.blit(miyeon_image, miyeon_rect)

    # Noodle resmini ekrana çiz (eğer görünürse)
    if noodle_visible:
        screen.blit(noodle_image, noodle_rect)

        # Noodle 3 saniye boyunca tıklanmazsa gizle
        current_time = time.time()
        if current_time - noodle_spawn_time >= 3:  # 3 saniye geçti mi?
            noodle_visible = False  # Noodle'ı gizle
            noodle_hide_time = current_time  # Gizleme zamanını kaydet
            print("Noodle 3 saniye boyunca tıklanmadı, gizlendi!")

    # Noodle resmini yeniden göster (17 saniye sonra)
    if not noodle_visible:
        current_time = time.time()
        if current_time - noodle_hide_time >= noodle_spawn_interval:
            noodle_visible = True  # Noodle'ı tekrar göster
            noodle_rect.topleft = get_random_position()  # Yeni rastgele konum (Miyeon'un üzerine gelmeyecek)
            noodle_spawn_time = current_time  # Noodle'ın göründüğü zamanı kaydet
            print("Noodle tekrar belirdi!")

    # Puanı göster
    score_text = font.render(f"Puan: {score}", True, BLACK)
    screen.blit(score_text, (int(WIDTH * 0.05), int(HEIGHT * 0.05)))  # Ekranın %5'ine göre konumlandır

    # Popularity Bar'ı çiz
    bar_fill_ratio = min(score / points_for_popularity, 1)  # Bar doluluk oranı (0-1 arası)
    bar_fill_width = int(bar_fill_ratio * popularity_bar_width)  # Bar doluluk genişliği

    # Bar çerçevesi (gri ve dışarıda)
    bar_frame_rect = pygame.Rect(popularity_bar_x - 2, popularity_bar_y - 2, popularity_bar_width + 4, popularity_bar_height + 4)
    draw_rounded_rect(screen, GRAY, bar_frame_rect, 10)

    # Bar doluluk (pembe ve yuvarlak köşeli)
    bar_fill_rect = pygame.Rect(popularity_bar_x, popularity_bar_y, bar_fill_width, popularity_bar_height)
    draw_rounded_rect(screen, PINK, bar_fill_rect, 10)

    # Popularity metni
    popularity_text = font.render(f"Popularity: {popularity}", True, BLACK)
    screen.blit(popularity_text, (popularity_bar_x, popularity_bar_y - int(HEIGHT * 0.05)))  # Barın üstüne yerleştir

    # 2x güç aktifse geri sayımı göster
    if power_active:
        elapsed_time = time.time() - power_start_time  # Geçen süre
        remaining_time = max(0, power_duration - elapsed_time)  # Kalan süre
        if remaining_time > 0:
            power_text = font.render(f"2x Güç: {int(remaining_time)} saniye", True, BLACK)
            screen.blit(power_text, (int(WIDTH * 0.05), int(HEIGHT * 0.1)))  # Ekranın %5'ine göre konumlandır
        else:
            power_active = False  # Süre doldu, gücü kapat
            click_power = 1  # Tıklama gücünü 1x yap
            print("2x Güç Sona Erdi!")

    pygame.display.update()

pygame.quit()
sys.exit()
