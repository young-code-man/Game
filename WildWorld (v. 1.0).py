import pygame, sys, math, random, noise, platform, os
from pygame.locals import *
pygame.init()

# Подключаем музыку
pygame.mixer.music.load('All_Sounds/main_music.wav')
pygame.mixer.music.play(-1)

# Работаем над главным окном и его отображением(его параметрами)
display_width = 1200
display_height = 1000
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("WildWorld")
over_ground = pygame.transform.scale(pygame.image.load("All_Pictures/overground_picture.jpg"),
                                     (display_width, display_height))
playerscale = 1
showHitBoxes = False          # Это места куда игрок может ударить по блокам и монсрам, чтобы их разрушить

# Загружаем иконку приложения
icon = pygame.image.load('All_Pictures/icon_picture.png')
pygame.display.set_icon(icon)


# В следующих функциях(до следующего комментария) мы просто загружаем картинки разного предназначения в программу
# и даем программе понять что с ней надо делать, плюс в некоторых случаях, редактируем картинку, подгоняя ее под мир
# еще загружаем некоторые изображения и указываем откуда их брать или если не нашли -> ошибка
def load_image(name):
    fullname = os.path.join('All_Pictures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def load_hp_icons():
    global hp_icons
    miscIconTilesheet = pygame.transform.scale(pygame.image.load("All_Pictures/HP_Pictures.png"), (50, 100))
    hp_icons = []
    for j in range(1):
        for i in range(2):
            surf = pygame.Surface((50, 50))
            surf.blit(miscIconTilesheet, (-i * 50, -j * 50))
            hp_icons.append(surf)

def load_weapon_images():
    global weapon_images
    itemTilesheet = pygame.transform.scale(pygame.image.load("All_Pictures/weapon_objects.png"),
                                           (int(BLOCKSIZE / 1.5 * 16), int(BLOCKSIZE / 1.5 * 16)))
    weapon_images = []
    for i in range(16):
        for j in range(16):
            surf = pygame.Surface((int(BLOCKSIZE / 1.5), int(BLOCKSIZE / 1.5)))
            surf.set_colorkey((255, 0, 255))
            surf.blit(itemTilesheet, (-j * (BLOCKSIZE / 1.5), -i * (BLOCKSIZE / 1.5)))
            weapon_images.append(surf)

def load_small_inv_picture():
    global small_inv_images
    small_inv = pygame.transform.scale(pygame.image.load("All_Pictures/weapon_objects.png"), (576, 576))
    small_inv_images = []
    for i in range(16):
        for j in range(16):
            surf = pygame.Surface((36, 36))
            surf.set_colorkey((255, 0, 255))
            surf.blit(small_inv, (-j * 36, -i * 36))
            small_inv_images.append(surf)

def load_player_picture():
    global player_pictures
    characterimages = pygame.transform.scale(pygame.image.load("All_Pictures/player_moving_picture.png"),
                                             (int(BLOCKSIZE * 4 * playerscale), int(BLOCKSIZE * 4 * playerscale)))
    characterimages.set_colorkey((66, 170, 255))
    player_pictures = []
    for i in range(2):
        for j in range(4):
            surf = pygame.Surface((BLOCKSIZE * playerscale, BLOCKSIZE * 2 * playerscale))
            surf.set_colorkey((255, 255, 255))
            surf.blit(characterimages, (-j * BLOCKSIZE * playerscale, -i * BLOCKSIZE * 2 * playerscale))
            player_pictures.append(surf)

def load_blocks_images():
    global blocks
    tilesheet = pygame.transform.scale(pygame.image.load("All_Pictures/blocks_objects.png"),
                                       (BLOCKSIZE * 16, BLOCKSIZE * 16))
    blocks = []
    for j in range(16):
        for i in range(16):
            surf = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
            surf.set_colorkey((255, 0, 255))
            surf.blit(tilesheet, (-i * BLOCKSIZE, -j * BLOCKSIZE))
            blocks.append(surf)

def load_back_bloks_pictures():
    global back_pictures
    back_blocks = pygame.transform.scale(pygame.image.load("All_Pictures/back_objects.png"),
                                         (BLOCKSIZE * 16, BLOCKSIZE * 16))
    back_pictures = []
    for j in range(16):
        for i in range(16):
            surf = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
            surf.blit(back_blocks, (-i * BLOCKSIZE, -j * BLOCKSIZE))
            back_pictures.append(surf)

def create_small_inv_background():
    global small_inv_back
    small_inv_back = pygame.Surface((610, 60))
    pygame.draw.rect(small_inv_back, (150, 150, 150), Rect(0, 0, 610, 60), 0)
    for i in range(10):
        pygame.draw.rect(small_inv_back, (200, 200, 200), Rect(i * 61, 0, 60, 60), 5)
    small_inv_back.set_alpha(200)



# На доработке... (функционал полностью рабочий, отдельно если, то запускается, сделано на основе гланого персонажа)
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.look_right = True
        self.size = 32
        size = self.size
        self.im = pygame.transform.scale(load_image(random.choice(['white_ghost.png'])), (size, size))
        self.run_mod()
        self.rects()
        super().__init__(all_sprites)
        super().__init__(evil_sprites)

        self.rect = self.image.get_rect()
        print(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y

        self.right_blocked, self.left_blocked = False, False

    def rects(self):
        grnd = pygame.sprite.Sprite()
        grnd.image = pygame.Surface([self.size // 2, 2])
        grnd.rect = pygame.Rect(self.size + 20, self.size, 1, 2)
        grnd.rect.x = self.x + self.size // 6
        grnd.rect.y = self.y + self.size
        self.grnd = grnd

        bodyr = pygame.sprite.Sprite()
        bodyr.image = pygame.Surface([1, self.size - 2])
        bodyr.rect = pygame.Rect(self.size, self.size, 10, 10)
        bodyr.rect.x = self.x + self.size * 5 // 7
        bodyr.rect.y = self.y
        self.bodyr = bodyr

        bodyl = pygame.sprite.Sprite()
        bodyl.image = pygame.Surface([1, self.size - 2])
        bodyl.rect = pygame.Rect(self.size + 20, self.size, 10, 10)
        bodyl.rect.x = self.x + self.size // 4
        bodyl.rect.y = self.y
        self.bodyl = bodyl

        top = pygame.sprite.Sprite()
        top.image = pygame.Surface([self.size // 2, 1])
        top.rect = pygame.Rect(self.size + 20, self.size, 1, 2)
        top.rect.x = self.x + self.size // 4
        top.rect.y = self.y
        self.top = top

    def run_mod(self):
        self.vx = 1  # скорость можно изменить
        self.run = True

        im = self.im
        if not self.look_right:
            im = pygame.transform.flip(
                im, True, False)
            self.vx *= -1
        self.image = im

    def update(self):
        if pygame.sprite.spritecollideany(self.top, hero_sprites):
            pass
        elif pygame.sprite.spritecollideany(self.bodyr, hero_sprites):
            self.vx = -20
            self.vy = -20
        elif pygame.sprite.spritecollideany(self.bodyl, hero_sprites):
            self.vx = 20
            self.vy = -20

        if pygame.sprite.spritecollideany(self.grnd, block_sprites):
            self.vy = 0

        elif not pygame.sprite.spritecollideany(self.grnd, block_sprites):
            self.vy = 3

        else:
            self.vy = 0
        if self.vx != 0 or self.vy != 0:
            self.right_blocked = pygame.sprite.spritecollideany(self.bodyr, block_sprites)
            self.left_blocked = pygame.sprite.spritecollideany(self.bodyl, block_sprites)

            if self.vx > 0 and self.right_blocked:
                self.look_right = False
                self.run_mod()
                if self.vx < 0 and self.left_blocked:
                    self.rect = self.rect.move(self.vx, self.vy)
                    self.grnd.rect = self.grnd.rect.move(self.vx, self.vy)
                    self.bodyr.rect = self.bodyr.rect.move(self.vx, self.vy)
                    self.bodyl.rect = self.bodyl.rect.move(self.vx, self.vy)
                    self.top.rect = self.top.rect.move(self.vx, self.vy)

            elif self.vx < 0 and self.left_blocked:
                self.look_right = True
                self.run_mod()

            self.rect = self.rect.move(self.vx, self.vy)
            self.grnd.rect = self.grnd.rect.move(self.vx, self.vy)
            self.bodyr.rect = self.bodyr.rect.move(self.vx, self.vy)
            self.bodyl.rect = self.bodyl.rect.move(self.vx, self.vy)
            self.top.rect = self.top.rect.move(self.vx, self.vy)

# Работа с отображенеим объектов в мире и просто работа с объектами мира
class world_object:
    def __init__(self, name, amnt, pos):
        global worldItems
        self.name = name
        self.tags = getTagsFromName(name)
        self.imgIndex = getItemImgIndex(name)
        self.pos = (pos[0] - BLOCKSIZE / 3, pos[1] - BLOCKSIZE / 3)
        self.rect = Rect(pos[0] - BLOCKSIZE / 3, pos[1] - BLOCKSIZE / 3, BLOCKSIZE / 1.5, BLOCKSIZE / 1.5)
        self.vel = (random.random() * 0.5 - 0.25, random.random() - 2)
        self.age = 0
        self.amnt = amnt
        worldItems.append(self)

    def update(self):
        global worldItems
        if self.age > 10000:
            worldItems.remove(self)
        else:
            self.age += 1
        if p.alive:
            if distance(self.pos, p.pos) < BLOCKSIZE * 3:
                self.vel = ((p.pos[0] - self.pos[0]) / 15, (p.pos[1] - self.pos[1]) / 15)
        self.vel = (self.vel[0], self.vel[1] + 0.2)
        self.vel = (self.vel[0] * 0.99, self.vel[1] * 0.99 + 0.05)
        if self.vel[1] > 5:
            self.vel = (self.vel[0], 5)
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.rect.left = self.pos[0] - BLOCKSIZE / 3
        self.rect.top = self.pos[1] - BLOCKSIZE / 3
        blockpos = (math.floor(self.rect.centerx // BLOCKSIZE), math.floor(self.rect.centery // BLOCKSIZE))
        for i in range(3):
            for j in range(3):
                val = world_data[blockpos[1] + j - 1 - CHUNKSIZE][blockpos[0] + i - 1 - CHUNKSIZE][0]
                if val not in uncollidableBlocks:
                    blockrect = Rect(BLOCKSIZE * (blockpos[0] + i - 1), BLOCKSIZE * (blockpos[1] + j - 1), BLOCKSIZE,
                                     BLOCKSIZE)
                    if blockrect.colliderect(self.rect):
                        deltaX = self.rect.centerx - blockrect.centerx
                        deltaY = self.rect.centery - blockrect.centery
                        if abs(deltaX) > abs(deltaY):
                            if deltaX > 0:
                                self.pos = (blockrect.right + BLOCKSIZE / 3, self.pos[1])
                                self.vel = (0, self.vel[1])
                            else:
                                self.pos = (blockrect.left - BLOCKSIZE / 3, self.pos[1])
                                self.vel = (0, self.vel[1])
                        else:
                            if deltaY > 0:
                                self.pos = (self.pos[0], blockrect.bottom + BLOCKSIZE / 3)
                                if self.vel[1] < 0:
                                    self.vel = (self.vel[0], 0)
                            else:
                                self.pos = (self.pos[0], blockrect.top - BLOCKSIZE / 3)
                                if self.vel[1] > 0:
                                    self.vel = (self.vel[0] * 0.5, 0)
        if p.alive:
            if p.rect.colliderect(self.rect):
                p.changeItem(self.name, self.amnt)
                worldItems.remove(self)

    def draw(self):
        display.blit(weapon_images[self.imgIndex], (int(self.rect.left - CAM.pos[0]), int(self.rect.top - CAM.pos[1])))


# Работа с объектами игр, настрока их имен(как для нас, так и для программы)
class objects:
    def __init__(self, name, amnt):
        self.name = name
        self.tags = getTagsFromName(name)
        self.amnt = amnt
        self.imgIndex = getItemImgIndex(name)


# Работаем с самой картой и ее постройкой и отображением всех элементов (также его загрузка)
class main_world:
    def __init__(self, x_chunks, y_chunks, chunk_size, block_size):
        self.CHUNKSIZE = chunk_size
        self.BLOCKSIZE = block_size
        self.x_chunks = x_chunks
        self.y_chunks = y_chunks
        self.chunks = []
        self.focusChunks = []
        self.createChunks()
        self.lightUpdateDelay = 10
        self.lightUpdateTick = 0

    def createChunks(self):
        self.chunks = []
        for i in range(self.y_chunks):
            self.chunks.append([])
            for j in range(self.x_chunks):
                self.chunks[i].append(Chunk(self.CHUNKSIZE, self.BLOCKSIZE,
                                            (j * self.CHUNKSIZE * self.BLOCKSIZE, i * self.CHUNKSIZE * self.BLOCKSIZE)))

    def generateTerrain(self, num):
        global world_data
        world_data = []
        for j in range(self.CHUNKSIZE * self.y_chunks):
            world_data.append([])
            for i in range(self.CHUNKSIZE * self.x_chunks):
                val = 400 - noise.noise((i * 500) / 10000, 0.0001, 0.235) * 15 + noise.noise((i * 100) / 10000, 0.0001,
                                                                                             0.235) * 15
                if j < val:
                    val = 0
                    backval = 0
                else:
                    if j < 500:
                        val = 2
                        backval = 2
                    else:
                        val = 1
                        backval = 1
                    if 400 < j == 2 and j <= 450:
                        backval = 2
                    if j > 0:
                        if world_data[j - 1][i][0] == 0 and val == 2:
                            val = 3
                            backval = 3
                        if world_data[j - 2][i][0] == 0 and val == 2:
                            backval = 3

                world_data[j].append([val, backval])
        print("Spawning stone...")
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 6)):  # surface stone
            ore(1, 6, None, (300, 425), (6, CHUNKNUMX * CHUNKSIZE - 6))
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 4)):  # lower stone
            ore(1, 6, None, (425, 500), (6, CHUNKNUMX * CHUNKSIZE - 6), 1)
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 4)):  # boarder stone
            ore(1, 6, None, (500, 500), (6, CHUNKNUMX * CHUNKSIZE - 6), 1)
        val = random.randint(50, CHUNKSIZE * CHUNKNUMX - 50)
        print("Spawning sand...")
        print("Spawning Ores...")
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 3)):  # coal
            ore(34, 4, None, None, (4, CHUNKNUMX * CHUNKSIZE - 4))
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 7)):  # iron,copper,lead
            ore(33, 3, None, None, (4, CHUNKNUMX * CHUNKSIZE - 4))
            ore(51, 3, None, None, (4, CHUNKNUMX * CHUNKSIZE - 4))
            ore(52, 3, None, None, (4, CHUNKNUMX * CHUNKSIZE - 4))
        print("Making Caves...")
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 12)):  # simple caves
            ore(0, 10, None, None, (10, CHUNKNUMX * CHUNKSIZE - 10))
        for i in range(int(CHUNKNUMX * CHUNKNUMY / 12)):  # bigger lower caves
            ore(0, 17, None, (550, CHUNKSIZE * CHUNKNUMY - 17), (17, CHUNKNUMX * CHUNKSIZE - 17))
        print("Adding Loot... (", int(CHUNKNUMX * CHUNKNUMY / 200), ")")
        print("Growing Trees...")
        for i in range(int(CHUNKNUMX * CHUNKSIZE / 3.5)):
            tree((random.randint(0, CHUNKNUMX * CHUNKSIZE), 150))

    def loadTerrain(self, num):
        global world_data
        data = open("maps\mapData" + str(num), "r")
        tData = data.readlines()
        world_data = []
        for i in range(len(tData)):
            world_data.append([])
            for j in range(int(len(tData[0]) / 6)):
                world_data[i].append([int(tData[i][j * 6:j * 6 + 3]), int(tData[i][j * 6 + 3:j * 6 + 6])])
            print(str(i / (len(tData)) * 100) + "%")
        data.close()

    def loadChunks(self, pos):
        camj = int((pos[0] + display_width / 2) // (BLOCKSIZE * CHUNKSIZE))
        cami = int((pos[1] + display_height / 2) // (BLOCKSIZE * CHUNKSIZE))
        for chunk in self.focusChunks:
            if chunk[0] < cami - 2 or chunk[0] > cami + 2:
                self.chunks[chunk[0]][chunk[1]].loaded = False
                self.chunks[chunk[0]][chunk[1]].surface = None
                self.chunks[chunk[0]][chunk[1]].blocks = None
            if chunk[1] < camj - 2 or chunk[1] > camj + 2:
                self.chunks[chunk[0]][chunk[1]].loaded = False
                self.chunks[chunk[0]][chunk[1]].surface = None
                self.chunks[chunk[0]][chunk[1]].blocks = None

        self.focusChunks = []
        for i in range(5):
            for j in range(5):
                cpos = (cami + i - 2, camj + j - 2)
                if 0 < cpos[0] < CHUNKNUMY and cpos[1] > 0 and cpos[1] < CHUNKNUMX:
                    self.focusChunks.append((cami + i - 2, camj + j - 2))
                    if not self.chunks[cpos[0]][cpos[1]].loaded:
                        self.chunks[cpos[0]][cpos[1]].loaded = True
                        self.chunks[cpos[0]][cpos[1]].loadBlocks()
                        self.chunks[cpos[0]][cpos[1]].surface = pygame.Surface(
                            (CHUNKSIZE * BLOCKSIZE, CHUNKSIZE * BLOCKSIZE))
                        self.chunks[cpos[0]][cpos[1]].surface.set_colorkey((255, 0, 255))
                        self.chunks[cpos[0]][cpos[1]].updateSurface()

    def draw(self, offset):
        for chunk in self.focusChunks:
            self.chunks[chunk[0]][chunk[1]].draw(offset)


# Поработаем с рудой и ее отображением и функционалом
def ore(val, size, pos, brangey, brangex, back=None):
    global world_data
    if pos is None:
        if brangey is not None:
            if brangex is not None:
                pos = (random.randint(brangex[0], brangex[1]), random.randint(brangey[0], brangey[1]))
            else:
                pos = (random.randint(size, CHUNKNUMX * CHUNKSIZE - size - 1), random.randint(brangey[0], brangey[1]))
        else:
            pos = (random.randint(size, CHUNKNUMX * CHUNKSIZE - size - 1),
                   random.randint(300, CHUNKNUMY * CHUNKSIZE - size - 1))
    if world_data[pos[1]][pos[0]][0] > 0:
        world_data[pos[1]][pos[0]][0] = val
        if back is not None:
            world_data[pos[1]][pos[0]][1] = back
        if random.randint(0, 10) <= size:
            ore(val, size - 1, (pos[0] - 1, pos[1]), None, None, back)
        if random.randint(0, 10) <= size:
            ore(val, size - 1, (pos[0] + 1, pos[1]), None, None, back)
        if random.randint(0, 10) <= size:
            ore(val, size - 1, (pos[0], pos[1] - 1), None, None, back)
        if random.randint(0, 10) <= size:
            ore(val, size - 1, (pos[0], pos[1] + 1), None, None, back)

# Самое сложное и интерсное, работа с маленькими кусочками объектов, а точнее блоков когда мы их ломаем
class Chunk:
    def __init__(self, chunk_size, block_size, POS):
        self.sources = None
        self.surface = None
        self.CHUNKSIZE = chunk_size
        self.BLOCKSIZE = block_size
        self.POS = POS
        self.blocks = []
        self.loaded = False

    def createRandomBlocks(self):
        self.blocks = []
        for i in range(self.CHUNKSIZE):
            self.blocks.append([])
            for j in range(self.CHUNKSIZE):
                self.blocks[i].append(Block(random.randint(0, 20), 0))

    def loadBlocks(self):
        self.blocks = []
        datai = int(self.POS[0] / (self.CHUNKSIZE * self.BLOCKSIZE)) - 1
        dataj = int(self.POS[1] / (self.CHUNKSIZE * self.BLOCKSIZE)) - 1
        for i in range(self.CHUNKSIZE):
            self.blocks.append([])
            for j in range(self.CHUNKSIZE):
                dat = world_data[dataj * self.CHUNKSIZE + j][datai * self.CHUNKSIZE + i]
                self.blocks[i].append(Block(dat[0], dat[1]))

    def draw(self, offset):
        if self.loaded:
            display.blit(self.surface, (self.POS[0] - offset[0], self.POS[1] - offset[1]))

    def updateLight(self):
        for source in self.sources:
            self.blocks[source[0]][source[1]].light = 1
            self.traversed = []
            self.fillLight(source, 1, 4)

    def fillLight(self, pos, val, size):
        if pos not in self.traversed:
            self.blocks[pos[0]][pos[1]].light = val
        else:
            return
        self.traversed.append(pos)
        if size <= 0:
            return
        if pos[0] > 0:
            if self.blocks[pos[0] - 1][pos[1]].val > 0:
                self.fillLight((pos[0] - 1, pos[1]), val * 0.6, size - 1)
            else:
                self.fillLight((pos[0] - 1, pos[1]), val * 0.8, size - 1)
        if pos[0] < CHUNKSIZE - 1:
            if self.blocks[pos[0] + 1][pos[1]].val > 0:
                self.fillLight((pos[0] + 1, pos[1]), val * 0.6, size - 1)
            else:
                self.fillLight((pos[0] + 1, pos[1]), val * 0.8, size - 1)
        if pos[1] > 0:
            if self.blocks[pos[0]][pos[1] - 1].val > 0:
                self.fillLight((pos[0], pos[1] - 1), val * 0.6, size - 1)
            else:
                self.fillLight((pos[0], pos[1] - 1), val * 0.8, size - 1)
        if pos[1] < CHUNKSIZE - 1:
            if self.blocks[pos[0]][pos[1] + 1].val > 0:
                self.fillLight((pos[0], pos[1] + 1), val * 0.6, size - 1)
            else:
                self.fillLight((pos[0], pos[1] + 1), val * 0.8, size - 1)

    def updateSurface(self):
        self.surface.fill((255, 0, 255))
        self.surface.set_colorkey((255, 0, 255))
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j].val in transparentBlocks:
                    if self.blocks[i][j].backval > 0:
                        self.surface.blit(back_pictures[self.blocks[i][j].backval],
                                          (self.BLOCKSIZE * i, self.BLOCKSIZE * j))
                        if self.blocks[i][j].backintegrity != self.blocks[i][j].maxbackintegrity:
                            if self.blocks[i][j].backval == 19 or self.blocks[i][j].backval == 20:
                                img = blocks[240 + math.floor(
                                    (self.blocks[i][j].maxbackintegrity - self.blocks[i][j].backintegrity) /
                                    self.blocks[i][j].maxbackintegrity * 3)]
                            else:
                                img = blocks[240 + math.floor(
                                    (self.blocks[i][j].maxbackintegrity - self.blocks[i][j].backintegrity) /
                                    self.blocks[i][j].maxbackintegrity * 9)]
                            img.set_alpha(200)
                            self.surface.blit(img, (self.BLOCKSIZE * i, self.BLOCKSIZE * j))
                if self.blocks[i][j].val > 0:
                    self.surface.blit(blocks[self.blocks[i][j].val], (self.BLOCKSIZE * i, self.BLOCKSIZE * j))
                    if self.blocks[i][j].integrity != self.blocks[i][j].maxintegrity:
                        img = blocks[240 + math.floor(
                            (self.blocks[i][j].maxintegrity - self.blocks[i][j].integrity) / self.blocks[i][
                                j].maxintegrity * 9)]
                        img.set_alpha(200)
                        self.surface.blit(img, (self.BLOCKSIZE * i, self.BLOCKSIZE * j))
                elif self.blocks[i][j].backval > 0:
                    self.surface.blit(back_pictures[self.blocks[i][j].backval],
                                      (self.BLOCKSIZE * i, self.BLOCKSIZE * j))
                    if self.blocks[i][j].backintegrity != self.blocks[i][j].maxbackintegrity:
                        if self.blocks[i][j].backval == 19 or self.blocks[i][j].backval == 20:
                            img = blocks[240 + math.floor(
                                (self.blocks[i][j].maxbackintegrity - self.blocks[i][j].backintegrity) / self.blocks[i][
                                    j].maxbackintegrity * 3)]
                        else:
                            img = blocks[240 + math.floor(
                                (self.blocks[i][j].maxbackintegrity - self.blocks[i][j].backintegrity) / self.blocks[i][
                                    j].maxbackintegrity * 9)]
                        img.set_alpha(200)
                        self.surface.blit(img, (self.BLOCKSIZE * i, self.BLOCKSIZE * j))


class Block:
    def __init__(self, val, backval):
        self.val = val
        self.backval = backval
        integ = getIntegFromVal(val)
        self.integrity = integ
        self.maxintegrity = integ
        if backval > 0:
            integ = getIntegFromVal(backval)
            self.backintegrity = integ
            self.maxbackintegrity = integ
        self.light = 1


class Cam:
    def __init__(self, Map, pos):
        self.pos = pos
        self.oldpos = (-1000, -1000)
        self.Map = Map
        self.updateDelay = 10
        self.updateTick = 0

    def update(self):
        if self.pos != self.oldpos:
            if self.updateTick > self.updateDelay:
                self.updateTick -= self.updateDelay
                self.Map.loadChunks(self.pos)
                self.oldpos = self.pos
            else:
                self.updateTick += 1

    def damageBlock(self, val, screenPos, tags):
        global world_data
        actualPos = (screenPos[0] + int(self.pos[0]), screenPos[1] + int(self.pos[1]))
        chunkPos = (actualPos[0] // (CHUNKSIZE * BLOCKSIZE), actualPos[1] // (CHUNKSIZE * BLOCKSIZE))
        inChunkPos = ((actualPos[0] - chunkPos[0] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE,
                      (actualPos[1] - chunkPos[1] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE)
        if "pickaxe" in tags:
            bval = CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val
            if bval > 0:
                if bval == 54 or bval == 55:
                    world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][0] = 0
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val = 0
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                    return
                if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity > 0:
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity -= val
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                    if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity <= 0:
                        info = getInfoFromVal(bval)
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val = 0
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                        world_object(info[0], 1, (
                            chunkPos[0] * CHUNKSIZE * BLOCKSIZE + inChunkPos[0] * BLOCKSIZE + 2 / 3 * BLOCKSIZE,
                            chunkPos[1] * CHUNKSIZE * BLOCKSIZE + inChunkPos[1] * BLOCKSIZE + 2 / 3 * BLOCKSIZE))
                        world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                            0] = 0
        if "axe" in tags:
            backval = CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval
            if backval == 19 or backval == 20:
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity -= val
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity <= 0:
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval = 0
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                    pos = ((actualPos[0] // BLOCKSIZE) - CHUNKSIZE, (actualPos[1] // BLOCKSIZE) - CHUNKSIZE)
                    world_data[pos[1]][pos[0]][1] = 0
                    chunksVisited = []
                    for i in range(20):
                        pos = (pos[0], pos[1] - 1)
                        if world_data[pos[1]][pos[0]][1] == 20 or world_data[pos[1]][pos[0]][1] == 21:
                            world_data[pos[1]][pos[0]][1] = 0
                            bchunkPos = (pos[0] // CHUNKSIZE + 1, pos[1] // CHUNKSIZE + 1)
                            if bchunkPos not in chunksVisited:
                                chunksVisited.append(bchunkPos)
                            binChunkPos = (pos[0] - bchunkPos[0] * CHUNKSIZE, pos[1] - bchunkPos[1] * CHUNKSIZE)
                            CAM.Map.chunks[bchunkPos[1]][bchunkPos[0]].blocks[binChunkPos[0]][
                                binChunkPos[1]].backval = 0
                            world_object("wood", random.randint(2, 3), (
                                (pos[0] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE,
                                (pos[1] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE))
                            if random.randint(0, 7) == 0:
                                world_object("acorn", 1, ((pos[0] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE,
                                                          (pos[1] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE))
                            if random.randint(0, 7) == 0:
                                world_object("acorn", 1, ((pos[0] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE,
                                                       (pos[1] + CHUNKSIZE) * BLOCKSIZE + BLOCKSIZE))
                        else:
                            for i in range(len(chunksVisited)):
                                CAM.Map.chunks[chunksVisited[i][1]][chunksVisited[i][0]].updateSurface()
        if "hammer" in tags:
            backval = CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval
            if backval != 0 and backval != 19 and backval != 20 and backval != 21:
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity -= val
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity <= 0:
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval = 0
                    world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][1] = 0
                    CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()

    def placeBlock(self, name, tags, screenPos):
        global world_data, chestData, tpressed
        actualPos = (screenPos[0] + int(self.pos[0]), screenPos[1] + int(self.pos[1]))
        blockpos = (actualPos[0] // BLOCKSIZE, actualPos[1] // BLOCKSIZE)
        if not tpressed:
            if "backwall" not in tags:
                if not Rect(p.pos[0] - CAM.pos[0] - BLOCKSIZE / 2, p.pos[1] - CAM.pos[1] - BLOCKSIZE, BLOCKSIZE,
                            BLOCKSIZE * 2).colliderect(
                    Rect(blockpos[0] * BLOCKSIZE - CAM.pos[0], blockpos[1] * BLOCKSIZE - CAM.pos[1], BLOCKSIZE,
                         BLOCKSIZE)):
                    if name == "acorn":
                        if tree((blockpos[0] - CHUNKSIZE, blockpos[1] - CHUNKSIZE)):
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE][blockpos[0] // CHUNKSIZE].loadBlocks()
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE - 1][blockpos[0] // CHUNKSIZE].loadBlocks()
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE + 1][blockpos[0] // CHUNKSIZE].loadBlocks()
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE][blockpos[0] // CHUNKSIZE].updateSurface()
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE - 1][blockpos[0] // CHUNKSIZE].updateSurface()
                            CAM.Map.chunks[blockpos[1] // CHUNKSIZE + 1][blockpos[0] // CHUNKSIZE].updateSurface()
                            tpressed = True
                            return True
                        else:
                            return False
                    val = getValFromName(name)
                    chunkPos = (actualPos[0] // (CHUNKSIZE * BLOCKSIZE), actualPos[1] // (CHUNKSIZE * BLOCKSIZE))
                    inChunkPos = ((actualPos[0] - chunkPos[0] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE,
                                  (actualPos[1] - chunkPos[1] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE)
                    if world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                        0] == 0:
                        canPlace = False
                        if world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                            1] != 0:
                            canPlace = True
                        elif \
                                world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE - 1][
                                    (actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                                    0] != 0:
                            canPlace = True
                        elif \
                                world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE + 1][
                                    (actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                                    0] != 0:
                            canPlace = True
                        elif \
                                world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][
                                    (actualPos[0] // BLOCKSIZE) - CHUNKSIZE - 1][
                                    0] != 0:
                            canPlace = True
                        elif \
                                world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][
                                    (actualPos[0] // BLOCKSIZE) - CHUNKSIZE + 1][
                                    0] != 0:
                            canPlace = True
                        if canPlace:
                            if val in chestBlocks:
                                chestData.append(
                                    [((actualPos[0] // BLOCKSIZE) - CHUNKSIZE, (actualPos[1] // BLOCKSIZE) - CHUNKSIZE),
                                     [[None for i in range(4)] for i in range(7)]])
                            CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val = val
                            integ = getIntegFromVal(val)
                            CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][
                                inChunkPos[1]].integrity = integ
                            CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][
                                inChunkPos[1]].maxintegrity = integ
                            CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                            world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][
                                (actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                                0] = val
                            return True
            else:
                val = getValFromName(name)
                chunkPos = (actualPos[0] // (CHUNKSIZE * BLOCKSIZE), actualPos[1] // (CHUNKSIZE * BLOCKSIZE))
                inChunkPos = ((actualPos[0] - chunkPos[0] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE,
                              (actualPos[1] - chunkPos[1] * CHUNKSIZE * BLOCKSIZE) // BLOCKSIZE)
                if world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][1] == 0:
                    canPlace = False
                    if world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE - 1][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                        1] != 0:
                        canPlace = True
                    elif \
                    world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE + 1][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                        1] != 0:
                        canPlace = True
                    elif \
                    world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE - 1][
                        1] != 0:
                        canPlace = True
                    elif \
                    world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE + 1][
                        1] != 0:
                        canPlace = True
                    if canPlace:
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval = val
                        integ = getIntegFromVal(val)
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][
                            inChunkPos[1]].backintegrity = integ
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][
                            inChunkPos[1]].maxbackintegrity = integ
                        CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                        world_data[(actualPos[1] // BLOCKSIZE) - CHUNKSIZE][(actualPos[0] // BLOCKSIZE) - CHUNKSIZE][
                            1] = val
                        return True
            return False

    def altclickBlock(self, screenPos, tags):
        actualPos = (screenPos[0] + int(self.pos[0]), screenPos[1] + int(self.pos[1]))
        pos = ((actualPos[0] // BLOCKSIZE) - CHUNKSIZE, (actualPos[1] // BLOCKSIZE) - CHUNKSIZE)
        if world_data[pos[1]][pos[0]][0] in chestBlocks:
            for i in range(len(chestData)):
                if chestData[i][0] == pos:
                    items = chestData[i][1]
                    p.openChest(pos, items)

    def render(self):
        self.Map.draw((self.pos[0], self.pos[1]))


def drawHoldingItem():
    m = pygame.mouse.get_pos()
    display.blit(small_inv_images[itemHolding.imgIndex], (m[0] - BLOCKSIZE / 3, m[1] - BLOCKSIZE / 3))
    if "tool" not in itemHolding.tags:
        text = font.render(str(itemHolding.amnt), True, (255, 255, 255))
        display.blit(text, (m[0] - text.get_width() / 2 + 15, m[1] + 5))


class Player:
    def __init__(self, pos, maxhp, movespeed):
        self.pos = pos
        self.vel = (0, 0)
        self.maxhp = maxhp
        self.hp = maxhp
        self.hpsurf = pygame.Surface((428, 50))
        self.hpsurf.set_colorkey((255, 0, 255))
        self.movespeed = movespeed
        self.rect = Rect(pos[0] - (BLOCKSIZE / 2) * playerscale, pos[1] - BLOCKSIZE * playerscale,
                         BLOCKSIZE * playerscale, BLOCKSIZE * 2 * playerscale)
        self.animationFrame = 0
        self.direction = 0
        self.animationTick = 0
        self.groundedTick = 0
        self.grounded = False
        self.hotbar = [None for i in range(10)]
        self.inventory = [[None for i in range(4)] for i in range(10)]
        self.coinSlots = [None for i in range(4)]
        self.ammoSlots = [None for i in range(4)]
        self.showInventory = False
        self.selectedItem = 0
        self.craftableItems = []
        self.itemList = []
        self.craftingMenuVel = 0
        self.craftingMenuPos = 600
        self.craftingSlotDelay = 0
        self.craftingTableInRange = False
        self.furnaceInRange = False
        self.anvilInRange = False
        self.chestItems = None
        self.alive = True
        self.craftItemName = ""
        self.craftItemComponents = []
        self.respawnTick = 0

    def drawHotbar(self):
        display.blit(small_inv_back, (10, 10))
        for i in range(10):
            if self.hotbar[i] != None:
                display.blit(small_inv_images[self.hotbar[i].imgIndex], (22 + i * 61, 20))
                if "tool" not in self.hotbar[i].tags:
                    text = font.render(str(self.hotbar[i].amnt), True, (255, 255, 255))
                    display.blit(text, (50 + i * 61 - text.get_width() / 2, 40))
        pygame.draw.rect(display, (255, 255, 0), Rect(10 + self.selectedItem * 61, 10, 60, 60), 5)

    def updateCraftableItems(self, findItem=None):
        self.itemList = []
        for i in range(10):
            if self.hotbar[i] != None:
                found = False
                for k in range(len(self.itemList)):
                    if self.hotbar[i].name == self.itemList[k].name:
                        self.itemList[k].amnt += self.hotbar[i].amnt
                        found = True
                        break
                if not found:
                    self.itemList.append(objects(self.hotbar[i].name, self.hotbar[i].amnt))
        for i in range(10):
            for j in range(4):
                if self.inventory[i][j] != None:
                    found = False
                    for k in range(len(self.itemList)):
                        if self.inventory[i][j].name == self.itemList[k].name:
                            self.itemList[k].amnt += self.inventory[i][j].amnt
                            found = True
                            break
                    if not found:
                        self.itemList.append(objects(self.inventory[i][j].name, self.inventory[i][j].amnt))
        found = False
        if findItem != None:
            for i in range(len(self.craftableItems)):
                if self.craftableItems[i][0].name == findItem.name:
                    found = True
                    self.craftingMenuPos = 600 - i * 60
        if not found:
            self.craftingMenuPos = 600

    def updateAnimationFrame(self):
        if self.animationTick < 0:
            self.animationTick += 7
            if self.animationFrame < 3:
                self.animationFrame += 1
            else:
                self.animationFrame = 0
        else:
            self.animationTick -= 1

    def getItemAmnt(self, itemName):
        amnt = 0
        for i in range(10):
            if self.hotbar[i] != None:
                if self.hotbar[i].name == itemName:
                    amnt += self.hotbar[i].amnt
        for i in range(10):
            for j in range(4):
                if self.inventory[i][j] != None:
                    if self.inventory[i][j].name == itemName:
                        amnt += self.inventory[i][j].amnt
        for i in range(4):
            if self.ammoSlots[i] != None:
                if self.ammoSlots[i].name == itemName:
                    amnt += self.ammoSlots[i].amnt
        for i in range(4):
            if self.coinSlots[i] != None:
                if self.coinSlots[i].name == itemName:
                    amnt += self.coinSlots[i].amnt
        return amnt

    def changeItem(self, name, amnt):
        for i in range(10):
            if self.hotbar[i] != None:
                if self.hotbar[i].name == name:
                    if self.hotbar[i].amnt < 999:
                        self.hotbar[i].amnt += amnt
                        if self.hotbar[i].amnt > 999:
                            amnt = p.hotbar[i].amnt - 999
                            self.hotbar[i].amnt = 999
                        elif self.hotbar[i].amnt <= 0:
                            self.hotbar[i] = None
                            return
                        else:
                            return
        for i in range(10):
            for j in range(4):
                if self.inventory[i][j] != None:
                    if self.inventory[i][j].name == name:
                        if self.inventory[i][j].amnt < 999:
                            self.inventory[i][j].amnt += amnt
                            if self.inventory[i][j].amnt > 999:
                                amnt = self.inventory[i][j].amnt - 999
                                self.inventory[i][j].amnt = 999
                            elif self.inventory[i][j].amnt <= 0:
                                self.inventory[i][j] = None
                                return
                            else:
                                return
        for i in range(10):
            if self.hotbar[i] == None:
                self.hotbar[i] = objects(name, amnt)
                return
        for i in range(10):
            for j in range(4):
                if self.inventory[i][j] == None:
                    self.inventory[i][j] = objects(name, amnt)
                    return

    def update(self):
        global stopRight, stopLeft, pressed, itemHolding, itemPos
        if not self.alive:
            if self.respawnTick > 0:
                self.respawnTick -= 1
            else:
                self.pos = spawnPoint
                self.alive = True
                self.hp = self.maxhp
        if self.grounded:
            if self.groundedTick <= 0:
                self.groundedTick += 7
                self.grounded = False
                stopRight = False
                stopLeft = False
            else:
                self.groundedTick -= 1
        if self.alive:
            if movingRight:
                if not stopRight:
                    self.direction = 0
                    self.updateAnimationFrame()
                    self.vel = (self.vel[0] + 1, self.vel[1])
                    self.chestOpen = False
                    self.showInventory = False
                    itemPos = None
            if movingLeft:
                if not stopLeft:
                    self.direction = 1
                    self.updateAnimationFrame()
                    self.vel = (self.vel[0] - 1, self.vel[1])
                    self.chestOpen = False
                    self.showInventory = False
                    itemPos = None
        if not movingLeft and not movingRight:
            self.animationFrame = 0
        if self.vel[0] < -self.movespeed:
            self.vel = (-self.movespeed, self.vel[1])
        if self.vel[0] > self.movespeed:
            self.vel = (self.movespeed, self.vel[1])
        if self.alive:
            self.vel = (self.vel[0] * 0.95, self.vel[1] * 0.99 + 0.3)
            self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.blockpos = (math.floor(self.pos[0] // BLOCKSIZE), math.floor(self.pos[1] // BLOCKSIZE))
        self.craftingTableInRange = False
        self.furnaceInRange = False
        self.anvilInRange = False
        for i in range(3):
            for j in range(3):
                val = world_data[self.blockpos[1] + j - 1 - CHUNKSIZE][self.blockpos[0] + i - 1 - CHUNKSIZE][0]
                if val == 84:
                    self.craftingTableInRange = True
                if val == 61:
                    self.furnaceInRange = True
                if val == 100:
                    self.anvilInRange = True
                try:
                    if val not in uncollidableBlocks:
                        blockrect = Rect(BLOCKSIZE * (self.blockpos[0] + i - 1), BLOCKSIZE * (self.blockpos[1] + j - 1),
                                         BLOCKSIZE, BLOCKSIZE)
                        if blockrect.colliderect(self.rect):
                            deltaX = self.pos[0] - blockrect.centerx
                            deltaY = self.pos[1] - blockrect.centery
                            if abs(deltaX) > abs(deltaY):
                                if deltaX > 0:
                                    if val != 5:
                                        self.pos = (blockrect.right + (BLOCKSIZE / 2) * playerscale, self.pos[1])
                                        self.vel = (0, self.vel[1])
                                        stopLeft = True
                                else:
                                    if val != 5:
                                        self.pos = (blockrect.left - (BLOCKSIZE / 2) * playerscale, self.pos[1])
                                        self.vel = (0, self.vel[1])
                                        stopRight = True
                            else:
                                if deltaY > 0:
                                    if val != 5:
                                        self.pos = (self.pos[0], blockrect.bottom + BLOCKSIZE * playerscale)
                                        if self.vel[1] < 0:
                                            self.vel = (self.vel[0], 0)
                                else:
                                    if val == 5:
                                        if self.vel[1] >= 0:
                                            if self.rect.bottom <= blockrect.top + 10:
                                                if not movingDown:
                                                    self.pos = (self.pos[0], blockrect.top - BLOCKSIZE * playerscale)
                                                    if self.vel[1] > 0:
                                                        self.vel = (self.vel[0] * 0.5, 0)
                                                    self.grounded = True
                                    else:
                                        self.pos = (self.pos[0], blockrect.top - BLOCKSIZE * playerscale)
                                        if self.vel[1] > 0:
                                            self.vel = (self.vel[0] * 0.5, 0)
                                        self.grounded = True
                except:
                    print("player out of map")
        self.rect.left = self.pos[0] - BLOCKSIZE / 2 * playerscale
        self.rect.top = self.pos[1] - BLOCKSIZE * playerscale

    def drawHP(self):
        heartNum = math.ceil(self.hp / 10)
        for i in range(heartNum):
            surf = pygame.Surface((50, 50))
            surf.set_colorkey((255, 0, 255))
            surf.blit(hp_icons[0], (0, 0))
            if i == heartNum - 1:
                surf.set_alpha(25.5 * (self.hp % 10))
            display.blit(surf, (display_width - 60 - i * 42, 15))
        font = pygame.font.SysFont("Fixedsys", 25)
        text = font.render("Life: " + str(self.hp) + "/" + str(self.maxhp), True, (255, 255, 255))
        display.blit(text, (display_width - 350, 3))

    def draw(self):
        display.blit(player_pictures[self.animationFrame + self.direction * 4],
                     (int(self.rect.left - CAM.pos[0]), int(self.rect.top - CAM.pos[1])))
        if showHitBoxes:
            pygame.draw.rect(display, (255, 0, 0),
                             Rect(self.rect.left - CAM.pos[0], self.rect.top - CAM.pos[1], self.rect.width,
                                  self.rect.height), 2)


def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def putItemBack(item):
    global itemPos
    if itemPos != None:
        if itemPos[0] == "inventory":
            p.inventory[itemPos[1][0]][itemPos[1][1]] = item
        elif itemPos[0] == "hotbar":
            p.hotbar[itemPos[1]] = item
        elif itemPos[0] == "coins":
            p.coinSlots[itemPos[1]] = item
        elif itemPos[0] == "ammo":
            p.ammoSlots[itemPos[1]] = item
        else:
            p.chestItems[itemPos[1][0]][itemPos[1][1]] = item
    else:
        p.changeItem(item.name, item.amnt)
    itemPos = None


def tree(pos):
    global world_data
    planted = False
    for i in range(1000):
        try:
            if world_data[pos[1] - 1][pos[0]][1] == 20:
                return False
            if world_data[pos[1] + 1][pos[0]][0] == 3:
                planted = True
                if world_data[pos[1]][pos[0]][1] != 19:
                    world_data[pos[1]][pos[0]][1] = 19
                    for i in range(12):
                        pos = (pos[0], pos[1] - 1)
                        world_data[pos[1]][pos[0]][1] = 20
                        if random.randint(0, 15) == 15 or i == 11:
                            world_data[pos[1]][pos[0]][1] = 21
                            break
                    break
        except:
            var = None
        pos = (pos[0], pos[1] + 1)
    if planted:
        return True
    else:
        return False


def updateWorldItems():
    global worldItems
    for item in worldItems:
        item.update()


def drawWorldItems():
    for item in worldItems:
        item.draw()


def getItemImgIndex(name):
    if name == "wood": return 4
    if name == "dirt": return 2
    if name == "stone": return 1
    if name == "copper": return 226
    if name == "iron": return 210
    if name == "coal": return 194
    if name == "copper bar": return 227
    if name == "copper pickaxe": return 106
    if name == "copper axe": return 107
    if name == "copper hammer": return 108
    if name == "copper sword": return 109
    if name == "acorn": return 39


def getTagsFromName(name):
    if name == "wood": return ["block", "material"]
    if name == "dirt": return ["block"]
    if name == "stone": return ["block", "material"]
    if name == "copper": return ["ore"]
    if name == "iron": return ["ore"]
    if name == "coal": return ["ore"]
    if name == "copper bar": return ["material"]
    if name == "copper pickaxe": return ["tool", "pickaxe"]
    if name == "copper axe": return ["tool", "axe"]
    if name == "copper hammer": return ["tool", "hammer"]
    if name == "copper sword": return ["tool", "sword"]
    if name == "acorn": return ["block"]


def getInfoFromVal(val):
    if val == 1: return ["cobble", ["material", "block"]]
    if val == 4: return ["wood", ["material", "block"]]
    if val == 2 or val == 3: return ["dirt", ["material", "block"]]
    if val == 5: return ["wood platform", ["block"]]
    if val == 32: return ["gold", ["ore"]]
    if val == 33: return ["iron", ["ore"]]
    if val == 34: return ["coal", ["ore", "material"]]
    if val == 16: return ["cobble", ["block"]]
    if val == 51: return ["copper", ["ore"]]


def getValFromName(name):
    if name == "stone": return 1
    if name == "dirt": return 2
    if name == "cobble": return 16
    if name == "wood": return 4


def getIntegFromVal(val):
    if val == 1: return 100
    if val == 2 or val == 3: return 75
    if val == 32: return 200
    if val == 33: return 175
    if val == 34: return 150
    if val == 35: return 150
    if val == 51: return 120
    if val == 16: return 100
    if val == 19: return 500
    if val == 20: return 500
    if val == 4: return 150
    if val == 84: return 200
    if val == 5: return 80
    if val == 61: return 200
    if val == 85: return 200
    if val == 86: return 200
    if val == 48: return 2000
    if val == 54 or val == 55: return 5
    if val == 50: return 150
    if val == 66: return 150
    if val == 67: return 150
    if val == 65: return 150
    if val == 64: return 250
    if val == 100: return 350
    if val == 52: return 200


def updateRecentPickups():
    global recentPickups
    for pickup in recentPickups:
        pickup[2] -= 1
        if pickup[2] < 0:
            recentPickups.remove(pickup)
    recentPickups = sorted(recentPickups, key=lambda x: x[2], reverse=True)


def drawRecentPickups():
    for i in range(len(recentPickups)):
        if recentPickups[i][2] > 90:
            font = pygame.font.SysFont("Fixedsys", int((100 - recentPickups[i][2]) * 2.8))
        else:
            font = pygame.font.SysFont("Fixedsys", 28)
        if recentPickups[i][1] > 1:
            text = font.render(recentPickups[i][0] + " (" + str(recentPickups[i][1]) + ")", False, recentPickups[i][4])
        else:
            text = font.render(recentPickups[i][0], False, recentPickups[i][4])
        if recentPickups[i][2] <= 25:
            text.set_alpha(recentPickups[i][2] / 25 * 255)
        display.blit(text, (
            recentPickups[i][3][0] - CAM.pos[0] - text.get_width() / 2,
            recentPickups[i][3][1] - CAM.pos[1] - 75 - i * 30))


def updateDamagePopUps():
    global damagePopUps
    for popup in damagePopUps:
        popup[2] -= 1
        if popup[2] < 0:
            damagePopUps.remove(popup)


def drawDamagePopUps():
    for i in range(len(damagePopUps)):
        if damagePopUps[i][2] > 90:
            font = pygame.font.SysFont("Fixedsys", int((100 - damagePopUps[i][2]) * 4))
        else:
            font = pygame.font.SysFont("Fixedsys", 40)
        text = font.render(str(damagePopUps[i][0]), False, damagePopUps[i][1])
        if damagePopUps[i][2] <= 25:
            text.set_alpha(damagePopUps[i][2] / 25 * 255)
        display.blit(text,
                     (damagePopUps[i][3][0] - CAM.pos[0] - text.get_width() / 2, damagePopUps[i][3][1] - CAM.pos[1]))

def updateProjectiles():
    global projectiles
    for projectile in projectiles:
        projectile.update()


def drawProjectiles():
    for projectile in projectiles:
        projectile.draw()


transparentBlocks = [84, 5, 85, 86, 54, 55, 100]
uncollidableBlocks = [0, 84, 61, 85, 86, 54, 55, 100]
chestBlocks = [85, 86]

projectiles = []

if platform.system() == "Darwin":
    font = pygame.font.SysFont("Text_Size/ARCADECLASSIC.TFF", 20)
else:
    font = pygame.font.Font("Text_Size/ARCADECLASSIC.TTF", 20)
clock = pygame.time.Clock()

basicRecipies = [
    ["wood", 1, [["wood backwall", 4]]],
    ["wood", 1, [["wood platform", 2]]],
    ["cobble", 1, [["cobble backwall", 4]]],
    ["wood platform", 2, [["wood", 1]]],
    ["crafting table", 1, [["wood", 10]]],
]

toolspeeds = {"copper": 4,
              "iron": 6,
              }

worldSize = "tiny"

worldSizes = {
    "tiny": [20, 70],  # 3 seconds to gen
    "small": [100, 80],  # 16 seconds to gen
    "medium": [200, 120],  # 50 seconds to gen
    "large": [400, 180],  # 146 seconds to gen
    "massive": [800, 240],  # >146 seconds
}

# Меню запуска и уже прогрузка игры и ее функционала
win = pygame.display.set_mode((1200, 1000))
win.fill((0, 180, 210))

class button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawMenuWindow():
    win.fill((0, 180, 210))
    greenButton.draw(win, (0, 0, 0))
    redButton.draw(win, (0, 0, 0))

def redrawGameWindow():
    win.fill((0, 0, 0))

greenButton = button((0, 255, 0), 490, 390, 250, 100, "Start")
redButton = button((255, 0, 0), 490, 510, 250, 100, "Quit")

game_state = "menu"
run = True
while run:
    if game_state == "menu":
        redrawMenuWindow()
    elif game_state == "game":
        redrawGameWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenButton.isOver(pos):
                    CHUNKSIZE = 10
                    BLOCKSIZE = 48

                    CHUNKNUMX = worldSizes[worldSize][0]
                    CHUNKNUMY = worldSizes[worldSize][1]

                    print("Worldsize: " + worldSize + " (" + str(CHUNKSIZE * CHUNKNUMX) + "x" + str(
                        CHUNKSIZE * CHUNKNUMY) + " blocks)")
                    PLAYERREACH = BLOCKSIZE * 5

                    LEFTBOARDER = CHUNKSIZE * BLOCKSIZE + BLOCKSIZE / 2
                    RIGHTBOARDER = CHUNKSIZE * BLOCKSIZE * CHUNKNUMX - BLOCKSIZE / 2
                    BOTBOARDER = CHUNKSIZE * BLOCKSIZE * CHUNKNUMY - BLOCKSIZE / 2
                    TOPBOARDER = CHUNKSIZE * BLOCKSIZE + BLOCKSIZE / 2

                    globalLighting = 1

                    worldItems = []
                    recentPickups = []
                    damagePopUps = []

                    stopRight = False
                    stopLeft = False
                    movingRight = False
                    movingLeft = False
                    movingDown = False
                    movingDownTimer = 0
                    pressed = False
                    altpressed = False
                    tpressed = False
                    t2pressed = False
                    itemHolding = None
                    itemPos = None
                    print("Loading images...")

                    load_blocks_images()
                    load_back_bloks_pictures()
                    load_player_picture()
                    load_small_inv_picture()
                    create_small_inv_background()
                    load_weapon_images()
                    load_hp_icons()

                    print("Initailizing Objects...")
                    spawnPoint = (BLOCKSIZE * CHUNKNUMX * CHUNKSIZE / 2, BLOCKSIZE * 395)
                    CAM = Cam(main_world(CHUNKNUMX, CHUNKNUMY, CHUNKSIZE, BLOCKSIZE),
                              (spawnPoint[0] - display_width / 2, spawnPoint[1]))
                    p = Player(spawnPoint, 100, 4)
                    print("Generating terrain...")
                    CAM.Map.generateTerrain(0)

                    print("Giving tools...")

                    p.hotbar[0] = objects("copper pickaxe", 1)
                    p.hotbar[1] = objects("copper axe", 1)
                    p.hotbar[2] = objects("copper hammer", 1)
                    p.hotbar[3] = objects("copper sword", 1)
                    print("Done! (In", pygame.time.get_ticks() / 1000, "seconds!)")
                    p.hp = 100  # <- Даем нашему кол-во жизней (1средце = 10xp)

                    while 1:
                        gameTick = pygame.time.get_ticks()
                        if movingDown:
                            if movingDownTimer > 0:
                                movingDownTimer -= 1
                                if movingDownTimer <= 0:
                                    movingDown = False
                            movingDownTimer
                        CAM.pos = (CAM.pos[0] + (p.pos[0] - display_width / 2 - CAM.pos[0]) * 0.05,
                                   CAM.pos[1] + (p.pos[1] - display_height / 2 - CAM.pos[1]) * 0.05)
                        rel = pygame.mouse.get_rel()
                        m = pygame.mouse.get_pos()
                        if p.pos[0] < LEFTBOARDER:
                            p.pos = (LEFTBOARDER, p.pos[1])
                        elif p.pos[0] > RIGHTBOARDER:
                            p.pos = (RIGHTBOARDER, p.pos[1])
                        if p.pos[1] < TOPBOARDER:
                            p.pos = (p.pos[0], TOPBOARDER)
                        elif p.pos[1] > BOTBOARDER:
                            p.pos = (p.pos[0], BOTBOARDER)
                        if CAM.pos[0] < LEFTBOARDER - BLOCKSIZE / 2:
                            CAM.pos = (LEFTBOARDER - BLOCKSIZE / 2, CAM.pos[1])
                        elif CAM.pos[0] > RIGHTBOARDER + BLOCKSIZE / 2 - display_width:
                            CAM.pos = (RIGHTBOARDER + BLOCKSIZE / 2 - display_width, CAM.pos[1])
                        if CAM.pos[1] < TOPBOARDER - BLOCKSIZE / 2:
                            CAM.pos = (CAM.pos[0], TOPBOARDER - BLOCKSIZE / 2)
                        elif CAM.pos[1] > BOTBOARDER + BLOCKSIZE / 2 - display_height:
                            CAM.pos = (CAM.pos[0], BOTBOARDER + BLOCKSIZE / 2 - display_height)
                        if pygame.mouse.get_pressed()[0] and p.alive:
                            if p.hotbar[p.selectedItem] != None:
                                tags = p.hotbar[p.selectedItem].tags
                                if distance((p.pos[0] - CAM.pos[0], p.pos[1] - CAM.pos[1]), m) < PLAYERREACH:
                                    if "tool" in tags:
                                        for i in range(len(p.hotbar[p.selectedItem].name)):
                                            if p.hotbar[p.selectedItem].name[i] == " ":
                                                toolset = p.hotbar[p.selectedItem].name[:i]
                                                break
                                        damage = toolspeeds[toolset]
                                        CAM.damageBlock(damage, m, tags)
                                    if "block" in tags:
                                        if CAM.placeBlock(p.hotbar[p.selectedItem].name, p.hotbar[p.selectedItem].tags,
                                                          m):
                                            p.hotbar[p.selectedItem].amnt -= 1
                                            if p.hotbar[p.selectedItem].amnt <= 0:
                                                p.hotbar[p.selectedItem] = None
                                        p.hotbar[p.selectedItem].amnt -= 0
                                        if p.hotbar[p.selectedItem].amnt == 0:
                                            p.hotbar[p.selectedItem] = None
                        else:
                            tpressed = False
                            t2pressed = False
                        if pygame.mouse.get_pressed()[2]:
                            if not altpressed:
                                altpressed = True
                                if p.hotbar[p.selectedItem] != None:
                                    tags = p.hotbar[p.selectedItem].tags
                                else:
                                    tags = []
                                CAM.altclickBlock(m, tags)
                        else:
                            altpressed = False
                        CAM.update()
                        p.update()

                        updateProjectiles()
                        updateWorldItems()
                        updateDamagePopUps()
                        updateRecentPickups()
                        display.fill((135 * globalLighting, 206 * globalLighting, 235 * globalLighting))
                        CAM.render()
                        drawRecentPickups()
                        drawDamagePopUps()
                        drawProjectiles()
                        if p.alive:
                            p.draw()
                        drawWorldItems()
                        if p.alive:
                            p.drawHotbar()
                            p.drawHP()
                        fps = clock.get_fps()
                        text = font.render(
                            str(int(fps)) + "fps  " + str(int(p.pos[0] // BLOCKSIZE)) + "x " + str(
                                int(p.pos[1] // BLOCKSIZE)) + "y", True,
                            (255, 255, 255))
                        display.blit(text, (display_width - 180, 0))
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == KEYDOWN:
                                if event.key == K_a:
                                    movingLeft = True
                                    stopLeft = False
                                if event.key == K_d:
                                    movingRight = True
                                    stopRight = False
                                if event.key == K_s:
                                    movingDown = True
                                if event.key == K_j:
                                    p.pos = spawnPoint
                                    print("respawning...")
                                if event.key == K_h:
                                    if showHitBoxes:
                                        showHitBoxes = False
                                    else:
                                        showHitBoxes = True
                                if event.key == K_u:
                                    p.kill()
                                if event.key == K_o:
                                    num = random.randint(0, 4)
                                if event.key == K_w or event.key == K_SPACE:
                                    if p.grounded:
                                        p.vel = (p.vel[0], -BLOCKSIZE / 3.4)
                                if event.key == K_1: p.selectedItem = 0
                                if event.key == K_2: p.selectedItem = 1
                                if event.key == K_3: p.selectedItem = 2
                                if event.key == K_4: p.selectedItem = 3
                                if event.key == K_5: p.selectedItem = 4
                                if event.key == K_6: p.selectedItem = 5
                                if event.key == K_7: p.selectedItem = 6
                                if event.key == K_8: p.selectedItem = 7
                                if event.key == K_9: p.selectedItem = 8
                                if event.key == K_0: p.selectedItem = 9
                            if event.type == KEYUP:
                                if event.key == K_a:
                                    movingLeft = False
                                if event.key == K_d:
                                    movingRight = False
                                if event.key == K_s:
                                    movingDownTimer = 10
                            if event.type == MOUSEBUTTONDOWN:
                                if event.button == 4:
                                    if p.showInventory:
                                        p.craftingMenuVel += 5
                                        p.craftingSlotDelay = 15
                                    else:
                                        if p.selectedItem > 0:
                                            p.selectedItem -= 1
                                        else:
                                            p.selectedItem = 9
                                if event.button == 5:
                                    if p.showInventory:
                                        p.craftingMenuVel -= 5
                                        p.craftingSlotDelay = 15
                                    else:
                                        if p.selectedItem < 9:
                                            p.selectedItem += 1
                                        else:
                                            p.selectedItem = 0
                        clock.tick(60)
                        pygame.display.flip()

                    if __name__ == '__main__':
                        pygame.init()
                        display = pygame.display.set_mode(size)
                        all_sprites = pygame.sprite.Group()
                        block_sprites = pygame.sprite.Group()
                        hero_sprites = pygame.sprite.Group()
                        evil_sprites = pygame.sprite.Group()
                        near_sprites = pygame.sprite.Group()

                        running = True
                        # для примера только 2 врага, а в игре их просто побольше нагенерировать с рандомными координатами
                        ghost = Ghost(150, 40)

                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_d:
                                        hero.look_right = True
                                        hero.run_mod()
                                if event.type == pygame.KEYUP:
                                    if event.key == pygame.K_d:
                                        hero.stay_mod()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_a:
                                        hero.look_right = False
                                        hero.run_mod()
                                    if event.key == pygame.K_w:
                                        hero.jump_mod()
                                if event.type == pygame.KEYUP:
                                    if event.key == pygame.K_a:
                                        hero.stay_mod()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x, y = event.pos
                                    print(hero.is_near(x, y))
                                    if hero.is_near(x, y):
                                        pass  # тут должен быть поиск блока с данными координатами и его уничтожение (пока что не могу сделать без мира)

                            k += 1
                            if k == 15:  # скорость абсолютно всего зависит от нагрузки кода, так что если будет слишком медленно, надо уменьшить порог к (5, например)
                                k = 0
                                display.fill((100, 20, 110))
                                hero.update()
                                ghost.update()
                                bloha.update()
                            all_sprites.draw(display)
                            pygame.display.flip()

                        while pygame.event.wait().type != pygame.QUIT:
                            pass
                        pygame.quit()
                    game_state = "game"
                if redButton.isOver(pos):
                    print("clicked the 2button")
                    run = False
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = (105, 105, 105)
                else:
                    greenButton.color = (0, 255, 0)
                if redButton.isOver(pos):
                    redButton.color = (105, 105, 105)
                else:
                    redButton.color = (255, 0, 0)
