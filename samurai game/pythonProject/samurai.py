import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((637, 358))
pygame.display.set_caption("Samurai game by Filippov")
icon = pygame.image.load("img/gameicon.jpg")
pygame.display.set_icon(icon)

bg = pygame.image.load("img/background.jpg")

walk_right = [
    pygame.image.load("img/walk_right/playerright1.png").convert_alpha(),
    pygame.image.load("img/walk_right/playerright2.png").convert_alpha(),
    pygame.image.load("img/walk_right/playerright3.png").convert_alpha(),
    pygame.image.load("img/walk_right/playerright4.png").convert_alpha()
]

walk_left = [
    pygame.image.load("img/walk_left/playerleft1.png").convert_alpha(),
    pygame.image.load("img/walk_left/playerleft2.png").convert_alpha(),
    pygame.image.load("img/walk_left/playerleft3.png").convert_alpha(),
    pygame.image.load("img/walk_left/playerleft4.png").convert_alpha()
]

enemy = pygame.image.load("img/enemy.png").convert_alpha()
enemy_list = []
enemyspeed = 7

player_anim_count = 0

player_speed = 8
player_x = 50
player_y = 280
watch_left = 0

is_jump = False
jump_count = 9

UserScore = 0
HighestScore = 0

enemy_timer = pygame.USEREVENT + 1
delay = random.randint(500, 3500)
pygame.time.set_timer(enemy_timer, delay)

ingamelable = pygame.font.Font('fonts/Oswald-VariableFont_wght.ttf', 20)
label = pygame.font.Font('fonts/Oswald-VariableFont_wght.ttf', 40)
lose_label = label.render('You lose', False, (255, 255, 255))
restart_label = label.render('Try again', False, (50, 200, 215))
restart_label_rect = restart_label.get_rect(topleft=(250, 140))
finish_label = label.render('Close', False, (50, 200, 215))
finish_label_rect = restart_label.get_rect(topleft=(250, 210))

shuriken = pygame.image.load("img/weapon.png").convert_alpha()
shuriken_list = []
shuriken_left = 10

gameplay = True

running = True
while running:

    shurikenlefttext = ingamelable.render('Shurikens left: ' + str(shuriken_left), False, (0, 0, 0))
    userscoretext = ingamelable.render('Your score: ' + str(UserScore), False, (0, 0, 0))
    screen.blit(bg, (0, 0))
    screen.blit(shurikenlefttext, (10, 10))
    screen.blit(userscoretext, (150, 10))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(enemy, el)
                el.x -= enemyspeed

                if el.x < -40:
                    enemy_list.pop(i)
                    UserScore -= 0.5

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
            watch_left = 1
        elif keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
            watch_left = 0
        elif watch_left == 1:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 400:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0
        player_anim_count += 1


        if shuriken_list:
            for (i, el) in enumerate(shuriken_list):
                screen.blit(shuriken, (el.x, el.y))
                el.x += 10

                if el.x > 650:
                    shuriken_list.pop(i)

                if enemy_list:
                    for (index, en) in enumerate(enemy_list):
                        if el.colliderect(en):
                            enemy_list.pop(index)
                            shuriken_list.pop(i)
                            UserScore += 1
                            delay = random.randint(200, 2500)
                            pygame.time.set_timer(enemy_timer, delay)
                            shuriken_left += 1
                            if UserScore > HighestScore:
                                HighestScore = UserScore

    else:
        screen.fill((27, 26, 25))
        screen.blit(lose_label, (250, 70))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(finish_label, finish_label_rect)
        score_user = label.render('Score: ' + str(UserScore), False, (250, 220, 40))
        score_highest = label.render('Highest score: ' + str(HighestScore), False, (250, 220, 40))
        screen.blit(score_user, (5, 5))
        screen.blit(score_highest, (350, 5))

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 50
            enemy_list.clear()
            shuriken_list.clear()
            UserScore = 0
            shuriken_left = 10

        mouse = pygame.mouse.get_pos()
        if finish_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemyheight = random.choice([280, 140])
            enemy_list.append(enemy.get_rect(topleft=(550, enemyheight)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_x and shuriken_left > 0:
            shuriken_list.append(shuriken.get_rect(topleft=(player_x + 20, player_y + 10)))
            shuriken_left -= 1

    clock.tick(60)
