# author: Yixiao Lan.

import pygame
from moviepy.editor import VideoFileClip
import random
import time
import sys

class scene1:
    def __init__(self, require_hana=1, screen_color=(255, 255, 255), hero_kokoro=3, curr_bgm='1', timer_intv=20):

        self.require_hana = require_hana  # hana number hero need to get.

        self.big_cache = {}

        # timer initialize
        self.timer_intv = timer_intv
        self.big_cache['timer'] = 99 #
        self.big_cache['timer_dec'] = self.timer_intv
        self.big_cache['update_timer'] = True
        self.big_cache['moon'] = False

        # pen initialize
        self.big_cache['boom_rain'] = False
        self.big_cache['boom_sprite_dct'] = {}
        self.big_cache['boom_quantity'] = 30
        self.big_cache['boom_lock'] = False
        self.big_cache['boom_timer'] = 300


        self.players_life_time = hero_kokoro # initial life time
        self.hana_period = 600 # if holding hanas, the number of hanas will dec when each period end
        self.fixed_time = 500 # when touch bomb, hero should be fixed.
        self.screen_color = screen_color
        pygame.init()
        pygame.display.set_caption('Chase - by Eathoublu')
        self.spr_scale = (100, 100) # player size
        self.spr_func_scale = (50, 50) # functional sprite size
        self.spr_info_scale = (25, 25) # information sprite size
        self.spr_info_scale_2 = (30, 30)
        self.spr_info_scale_3 = (40, 40) # avatar size
        self.w, self.h = 1024, 768 # canvas size
        self.x_bound = (0, self.w-100) # player's bound x
        self.y_bound = (0, self.h-100) # player's bound y
        pygame.display.set_mode((self.w, self.h))
        self.screen = pygame.display.get_surface()
        self.load_spr_hero() # load hero
        self.load_spr_princess() # load princess
        self.load_spr_func() # load functional spr,but just in a lst.
        self.load_spr_effect() # init containers for effect
        self.load_spr_information() # load spr for information display
        self.data_initializer() # init function count dict which is to record the functional object the players eat.
        self.init_screen() # make the screen the initial state.

        # sound
        # self.play_bgm('1')
        self.load_sound_effect()
        self.curr_bgm = curr_bgm




        self.move_intv = 7 # move length per interval for hero
        self.move_intv_princess = 7 # move length for princess
        self.move_intv_origin = 7 # origin move intv

        self.func_intv = self.func_intv_constant = 100 # functional sprite appear interval

        self.max_functional_sprite = 50 # max sprite on screen

        self.hana_disappear_timer = 600







    def play_bgm(self, filename):
            pygame.mixer.init()
            pygame.mixer.music.load('assets/{}.mp3'.format(filename))
            pygame.mixer.music.play(-1, 0)

            # sound = pygame.mixer.Sound('assets/{}.mp3'.format('rain'))
            # sound.play()




    def stop_play_sound(self):
        pygame.mixer.music.stop()

    def load_sound_effect(self):
        sound_lst = [
            'pick',
            'pick2',
            'rain',
            'drop',
            'boom',
            'choose',
            'switch',
            'beep1',
            'beep2',
            'beep3',
            'fail',
            'magic'
        ]
        self.sound_dct = {}
        for sound in sound_lst:
            self.sound_dct[sound] = pygame.mixer.Sound('assets/{}.mp3'.format(sound))
        pass


    def play_sound_effect(self, sound_name):
        self.sound_dct[sound_name].play()



    def data_initializer(self):
        self.function_count = {'hero': {'red_hana': {'count':0, 'timer':0},
                               'blue_hana': {'count':0, 'timer':0},
                               'yellow_hana':{'count':0, 'timer':0},
                                       'fragrant': 0,
                                       'cake': 0,
                                        'star':0,
                                        'tree':0,
                                        'moon':0,
                                        'carrot':0,
                                        'heel':0,
                                        'wine':0,
                                        'fish':0,
                                        'candle':0,
                                        'piano':0,
                                        'pen':0,
                                        'bomb': 0,
                                        'kokoro':0,
                               },
                               'princess':  {'red_hana': {'count':0, 'timer':0},
                               'blue_hana': {'count':0, 'timer':0},
                               'yellow_hana':{'count':0, 'timer':0},
                               'fragrant': 0,
                               'cake': 0,
                                             'star': 0,
                                             'tree': 0,
                                             'moon': 0,
                                             'carrot': 0,
                                             'heel': 0,
                                             'wine': 0,
                                             'fish': 0,
                                             'candle': 0,
                                             'piano': 0,
                                             'pen': 0,
                                             'bomb': 0,
                                             'kokoro':0,
                               }
                               }

        pass


    def init_screen(self):
        # do it every loop and in init function
        self.screen.fill(self.screen_color)

    def load_image(self, path, scale):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, scale)
        return image

    def load_spr_information(self):
        # all information display should register in here first

        self.information_spr_dict = {}

        # create_group
        self.information_group = pygame.sprite.Group()
        self.num_img_lst = []
        # load numbers imgs
        for num in range(11):
            self.num_img_lst.append(self.load_image('assets/{}.PNG'.format(num), self.spr_info_scale))

        # for princess
        # avatar
        self.princess_avatar = pygame.sprite.Sprite()
        image = self.load_image('assets/avatar.PNG', self.spr_info_scale_3)
        self.princess_avatar.image = image
        self.princess_avatar.rect = image.get_rect()
        self.princess_avatar.rect.x = self.x_bound[1] - 250
        self.princess_avatar.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_avatar)

        # moon
        self.princess_moon = pygame.sprite.Sprite()
        image = self.load_image('assets/blank.PNG', self.spr_info_scale_2)
        self.princess_moon.image = image
        self.princess_moon.rect = image.get_rect()
        self.princess_moon.rect.x = self.x_bound[1] - 180
        self.princess_moon.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_moon)
        self.information_spr_dict['princess_moon'] = self.princess_moon

        self.blank_moon = self.load_image('assets/blank.PNG', self.spr_info_scale_2)
        self.display_moon = self.load_image('assets/moon.PNG', self.spr_info_scale_2)


        # kokoro
        self.princess_kokoro = pygame.sprite.Sprite()
        image = self.load_image('assets/kokoro.PNG', self.spr_info_scale)
        self.princess_kokoro.image = image
        self.princess_kokoro.rect = image.get_rect()
        self.princess_kokoro.rect.x = self.x_bound[1] - 150
        self.princess_kokoro.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_kokoro)
        # self.information_spr_dict['hero_kokoro'] = self.princess_kokoro

        # kokoro count
        self.princess_kokoro_count = pygame.sprite.Sprite()
        self.princess_kokoro_count.image = self.num_img_lst[10]
        self.princess_kokoro_count.rect = self.num_img_lst[10].get_rect()
        self.princess_kokoro_count.rect.x = self.x_bound[1] - 125
        self.princess_kokoro_count.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_kokoro_count)
        # self.information_spr_dict['hero_kokoro_count'] = self.hero_kokoro_count

        # fish
        self.princess_fish = pygame.sprite.Sprite()
        image = self.load_image('assets/fish.PNG', self.spr_info_scale)
        self.princess_fish.image = image
        self.princess_fish.rect = image.get_rect()
        self.princess_fish.rect.x = self.x_bound[1] - 100
        self.princess_fish.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_fish)
        self.information_spr_dict['princess_fish'] = self.princess_fish

        # fish count
        self.princess_fish_count = pygame.sprite.Sprite()
        self.princess_fish_count.image = self.num_img_lst[0]
        self.princess_fish_count.rect = self.num_img_lst[0].get_rect()
        self.princess_fish_count.rect.x = self.x_bound[1] - 75
        self.princess_fish_count.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_fish_count)
        self.information_spr_dict['princess_fish_count'] = self.princess_fish_count

        # tree
        self.princess_tree = pygame.sprite.Sprite()
        image = self.load_image('assets/tree.PNG', self.spr_info_scale)
        self.princess_tree.image = image
        self.princess_tree.rect = image.get_rect()
        self.princess_tree.rect.x = self.x_bound[1] - 50
        self.princess_tree.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_tree)
        self.information_spr_dict['princess_tree'] = self.princess_tree

        # tree count
        self.princess_tree_count = pygame.sprite.Sprite()
        self.princess_tree_count.image = self.num_img_lst[0]
        self.princess_tree_count.rect = self.num_img_lst[0].get_rect()
        self.princess_tree_count.rect.x = self.x_bound[1] - 25
        self.princess_tree_count.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_tree_count)
        self.information_spr_dict['princess_tree_count'] = self.princess_tree_count

        # carrot
        self.princess_carrot = pygame.sprite.Sprite()
        image = self.load_image('assets/carrot.PNG', self.spr_info_scale)
        self.princess_carrot.image = image
        self.princess_carrot.rect = image.get_rect()
        self.princess_carrot.rect.x = self.x_bound[1] - 0
        self.princess_carrot.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_carrot)
        self.information_spr_dict['princess_carrot'] = self.princess_carrot


        #  carrot count
        self.princess_carrot_count = pygame.sprite.Sprite()
        self.princess_carrot_count.image = self.num_img_lst[0]
        self.princess_carrot_count.rect = self.num_img_lst[0].get_rect()
        self.princess_carrot_count.rect.x = self.x_bound[1] - (-25)
        self.princess_carrot_count.rect.y = self.y_bound[0] + 50
        self.information_group.add(self.princess_carrot_count)
        self.information_spr_dict['princess_carrot_count'] = self.princess_carrot_count



        # for hero
        # avatar
        self.hero_avatar = pygame.sprite.Sprite()
        image = self.load_image('assets/_avatar.PNG', self.spr_info_scale_3)
        self.hero_avatar.image = image
        self.hero_avatar.rect = image.get_rect()
        self.hero_avatar.rect.x = self.x_bound[1] - 250
        self.hero_avatar.rect.y = self.y_bound[0] + 96
        self.information_group.add(self.hero_avatar)


        # fragrant
        self.hero_fragrant = pygame.sprite.Sprite()
        image = self.load_image('assets/blank.PNG', self.spr_info_scale_2)
        self.hero_fragrant.image = image
        self.hero_fragrant.rect = image.get_rect()
        self.hero_fragrant.rect.x = self.x_bound[1] - 180
        self.hero_fragrant.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_fragrant)
        self.information_spr_dict['hero_fragrant'] = self.hero_fragrant

        # cake
        self.hero_cake = pygame.sprite.Sprite()
        image = self.load_image('assets/blank.PNG', self.spr_info_scale_2)
        self.hero_cake.image = image
        self.hero_cake.rect = image.get_rect()
        self.hero_cake.rect.x = self.x_bound[1] - 210
        self.hero_cake.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_cake)
        self.information_spr_dict['hero_cake'] = self.hero_cake

        self.information_cake_image = self.load_image('assets/cake.PNG', self.spr_info_scale_2)
        self.information_fragrant_image = self.load_image('assets/candle.PNG', self.spr_info_scale_2)
        self.information_blank_image = self.load_image('assets/blank.PNG', self.spr_info_scale_2)

        # kokoro
        self.hero_kokoro = pygame.sprite.Sprite()
        image = self.load_image('assets/kokoro.PNG', self.spr_info_scale)
        self.hero_kokoro.image = image
        self.hero_kokoro.rect = image.get_rect()
        self.hero_kokoro.rect.x = self.x_bound[1] - 150
        self.hero_kokoro.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_kokoro)
        self.information_spr_dict['hero_kokoro'] = self.hero_kokoro

        # kokoro count
        self.hero_kokoro_count = pygame.sprite.Sprite()
        self.hero_kokoro_count.image = self.num_img_lst[self.hero.life if self.hero.life < 10 else 10]
        self.hero_kokoro_count.rect = self.num_img_lst[self.hero.life if self.hero.life < 10 else 10].get_rect()
        self.hero_kokoro_count.rect.x = self.x_bound[1] - 125
        self.hero_kokoro_count.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_kokoro_count)
        self.information_spr_dict['hero_kokoro_count'] = self.hero_kokoro_count


        # red hana
        self.hero_red_hana = pygame.sprite.Sprite()
        image = self.load_image('assets/red_hana.PNG', self.spr_info_scale)
        self.hero_red_hana.image = image
        self.hero_red_hana.rect = image.get_rect()
        self.hero_red_hana.rect.x = self.x_bound[1] - 100
        self.hero_red_hana.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_red_hana)
        self.information_spr_dict['hero_red_hana'] = self.hero_red_hana


        # red hana count
        self.hero_red_hana_count = pygame.sprite.Sprite()
        self.hero_red_hana_count.image = self.num_img_lst[0]
        self.hero_red_hana_count.rect = self.num_img_lst[0].get_rect()
        self.hero_red_hana_count.rect.x = self.x_bound[1] - 75
        self.hero_red_hana_count.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_red_hana_count)
        self.information_spr_dict['hero_red_hana_count'] = self.hero_red_hana_count

        # yellow hana
        self.hero_yellow_hana = pygame.sprite.Sprite()
        image = self.load_image('assets/yellow_hana.PNG', self.spr_info_scale)
        self.hero_yellow_hana.image = image
        self.hero_yellow_hana.rect = image.get_rect()
        self.hero_yellow_hana.rect.x = self.x_bound[1] - 50
        self.hero_yellow_hana.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_yellow_hana)
        self.information_spr_dict['hero_yellow_hana'] = self.hero_yellow_hana

        # yellow hana count
        self.hero_yellow_hana_count = pygame.sprite.Sprite()
        self.hero_yellow_hana_count.image = self.num_img_lst[0]
        self.hero_yellow_hana_count.rect = self.num_img_lst[0].get_rect()
        self.hero_yellow_hana_count.rect.x = self.x_bound[1] - 25
        self.hero_yellow_hana_count.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_yellow_hana_count)
        self.information_spr_dict['hero_yellow_hana_count'] = self.hero_yellow_hana_count

        # blue hana
        self.hero_blue_hana = pygame.sprite.Sprite()
        image = self.load_image('assets/blue_hana.PNG', self.spr_info_scale)
        self.hero_blue_hana.image = image
        self.hero_blue_hana.rect = image.get_rect()
        self.hero_blue_hana.rect.x = self.x_bound[1] - 0
        self.hero_blue_hana.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_blue_hana)
        self.information_spr_dict['hero_blue_hana'] = self.hero_blue_hana

        # blue hana count
        self.hero_blue_hana_count = pygame.sprite.Sprite()
        self.hero_blue_hana_count.image = self.num_img_lst[0]
        self.hero_blue_hana_count.rect = self.num_img_lst[0].get_rect()
        self.hero_blue_hana_count.rect.x = self.x_bound[1] - (-25)
        self.hero_blue_hana_count.rect.y = self.y_bound[0] + 100
        self.information_group.add(self.hero_blue_hana_count)
        self.information_spr_dict['hero_blue_hana_count'] = self.hero_blue_hana_count




        # public
        self.curr_level = pygame.sprite.Sprite()
        curr_level_img = self.load_image('assets/{}.PNG'.format(self.require_hana), (100, 100))
        self.curr_level.image = curr_level_img
        self.curr_level.rect = curr_level_img.get_rect()
        self.curr_level.rect.x = 10
        self.curr_level.rect.y = 10
        self.information_group.add(self.curr_level)

        self.can_chase_note = pygame.sprite.Sprite()
        self.blank_img = self.load_image('assets/blank.PNG', (100, 100))
        self.can_chase_kokoro_img = self.load_image('assets/kokoro.PNG', (100, 100))
        self.can_chase_note.image = self.blank_img
        self.can_chase_note.rect = self.blank_img.get_rect()
        self.can_chase_note.rect.x = 10
        self.can_chase_note.rect.y = 600
        self.information_group.add(self.can_chase_note)

        # timer
        self.timer_shi = pygame.sprite.Sprite()
        self.timer_shi.image = self.num_img_lst[int(str(self.big_cache['timer'])[0])]
        self.timer_shi.rect = self.num_img_lst[int(str(self.big_cache['timer'])[0])].get_rect()
        self.timer_shi.rect.x = self.w/2 - 50
        self.timer_shi.rect.y = 50
        self.information_group.add(self.timer_shi)

        self.timer_ge = pygame.sprite.Sprite()
        self.timer_ge.image = self.num_img_lst[int(str(self.big_cache['timer'])[1])]
        self.timer_ge.rect = self.num_img_lst[int(str(self.big_cache['timer'])[1])].get_rect()
        self.timer_ge.rect.x = self.w / 2 + 25 - 50
        self.timer_ge.rect.y = 50
        self.information_group.add(self.timer_ge)



















    def load_spr_effect(self):
        self.effect_group = pygame.sprite.Group()
        self.effect_group_lst = []


    def load_spr_func(self):
        self.func_spr_img = [self.load_image('assets/boom.PNG', self.spr_func_scale),
                         self.load_image('assets/kokoro.PNG', self.spr_func_scale),
                         self.load_image('assets/yellow_hana.PNG', self.spr_func_scale),
                         self.load_image('assets/blue_hana.PNG', self.spr_func_scale),
                         self.load_image('assets/fragrant.PNG', self.spr_func_scale),
                         self.load_image('assets/cake.PNG', self.spr_func_scale),
                         self.load_image('assets/bomb.PNG', self.spr_func_scale),
                         self.load_image('assets/red_hana.PNG', self.spr_func_scale),
                         self.load_image('assets/star.PNG', self.spr_func_scale),
                         self.load_image('assets/tree.PNG', self.spr_func_scale),
                         self.load_image('assets/moon.PNG', self.spr_func_scale),
                         self.load_image('assets/carrot.PNG', self.spr_func_scale),
                         self.load_image('assets/heel.PNG', self.spr_func_scale),
                         self.load_image('assets/wine.PNG', self.spr_func_scale),
                         self.load_image('assets/fish.PNG', self.spr_func_scale),
                         self.load_image('assets/candle.PNG', self.spr_func_scale),
                         self.load_image('assets/piano.PNG', self.spr_func_scale),
                         self.load_image('assets/pen.PNG', self.spr_func_scale),
                         ]
        self.func_group = pygame.sprite.Group()
        self.func_spr_lst = []
        self.destroy_later_lst = []

        self.idx_spr_dct = {0: 'boom',
                            1: 'kokoro',
                            2: 'yellow_hana',
                            3: 'blue_hana',
                            4: 'fragrant',
                            5: 'cake',
                            6: 'bomb',
                            7: 'red_hana',
                            8: 'star',
                            9: 'tree',
                            10: 'moon',
                            11: 'carrot',
                            12: 'heel',
                            13: 'wine',
                            14: 'fish',
                            15: 'candle',
                            16: 'pinao',
                            17: 'pen'
                            }

        self.spr_idx_dct = dict([[self.idx_spr_dct[k], k] for k in self.idx_spr_dct])
        # print(self.spr_idx_dct)


    def load_spr_hero(self):

        # load hero,and add him into player group
        self.hero_img = [self.load_image('assets/_main.PNG', self.spr_scale),
                         self.load_image('assets/_main2.PNG', self.spr_scale),
                         self.load_image('assets/_main3.PNG', self.spr_scale),
                         self.load_image('assets/_like.PNG', self.spr_scale),
                         self.load_image('assets/_die.PNG', self.spr_scale),
                         self.load_image('assets/_magic.PNG', self.spr_scale),
                         self.load_image('assets/_magic2.PNG', self.spr_scale)
                    ]
        self.curr_hero_state = 0

        self.hero = pygame.sprite.Sprite()
        self.hero.image = self.hero_img[self.curr_hero_state]
        self.hero.rect = self.hero_img[self.curr_hero_state].get_rect()
        self.hero.rect.x = self.w/2
        self.hero.rect.y = self.h/2
        self.hero.w = 30
        self.hero.y = 30

        self.hero.life = self.players_life_time
        self.hero.can_update = True
        self.hero.pause_time = 0
        self.hero.name = 'hero'
        self.hero.can_chase_princess = False
        self.hero.can_magic = True
        self.hero.can_boom = True
        self.hero.super_fast = False # switch with heels




        # print(self.hero.rect.h, self.hero.rect.w)

        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.hero)

        self.exit_flag = False

    def load_spr_princess(self):
        # like hero's
        self.princess_img = [self.load_image('assets/main.PNG', self.spr_scale),
                         self.load_image('assets/main2.PNG', self.spr_scale),
                         self.load_image('assets/main3.PNG', self.spr_scale),
                         self.load_image('assets/doki.PNG', self.spr_scale),
                         self.load_image('assets/die.PNG', self.spr_scale),
                    ]
        self.curr_princess_state = 0

        self.princess = pygame.sprite.Sprite()
        self.princess.image = self.princess_img[self.curr_princess_state]
        self.princess.rect = self.princess_img[self.curr_princess_state].get_rect()
        self.princess.rect.x = self.w/2
        self.princess.rect.y = self.h/2
        self.princess.w = 30
        self.princess.y = 30

        self.princess.life = self.players_life_time
        self.princess.can_update = True
        self.princess.pause_time = 0
        self.princess.name = 'princess'
        self.princess.can_boom = True
        self.princess.super_fast = False

        # print(self.hero.rect.h, self.hero.rect.w)

        # self.player_group = pygame.sprite.Group()
        self.player_group.add(self.princess)


    def update_hero_magic(self):
        # update the image of hero,make him like walking. when key pressed.
        self.play_sound_effect('magic')
        update_list = [5,6]
        if self.curr_hero_state != 0:
            self.curr_hero_state = 0
        else:
            self.curr_hero_state = 1
        self.hero.image = self.hero_img[update_list[self.curr_hero_state]]
        if self.hero.can_magic:
            while self.func_spr_lst:
                destroy_spr = self.func_spr_lst.pop(random.randint(0, len(self.func_spr_lst) - 1))
                destroy_spr.remove(self.func_group)
            self.hero.can_magic = False



    def update_hero(self):
        # update the image of hero,make him like walking. when key pressed.
        update_list = [0,1,2,1]
        if self.curr_hero_state != 3:
            self.curr_hero_state += 1
        else:
            self.curr_hero_state = 0
        self.hero.image = self.hero_img[update_list[self.curr_hero_state]]


    def update_princess(self):
        # like hero's
        update_list = [0,1,2,1]
        if self.curr_princess_state != 3:
            self.curr_princess_state += 1
        else:
            self.curr_princess_state = 0
        self.princess.image = self.princess_img[update_list[self.curr_princess_state]]

    def functional_update_hero(self):
        # call in every loop,if hero is paused, it can update his status.
        if not self.hero.can_update:
            if self.hero.pause > 0:
                self.hero.pause -= 1
            if self.hero.pause == 0:
                self.hero.can_update = True

    def functional_update_princess(self):
        # call in every loop,if hero is paused, it can update his status.
        if not self.princess.can_update:
            if self.princess.pause > 0:
                self.princess.pause -= 1
            if self.princess.pause == 0:
                self.princess.can_update = True

    def update_effect(self):
        # update the effect sprite in every loop
        delete_lst = []
        count = 0
        if self.effect_group_lst:
            for effect in self.effect_group:
                effect.pause -= 1
                if effect.pause == 0:
                    effect.remove(self.effect_group)
                    delete_lst.append(count)
            count += 1
        new_effect_group = []
        for idx in range(len(self.effect_group_lst)):
            if idx not in delete_lst:
                new_effect_group.append(self.effect_group_lst[idx])
        self.effect_group_lst = new_effect_group




    def check_hero_outbound(self):
        # if hero is out of bound, than make him randomly appear within canvas, otherwise do nothing.
        if self.hero.rect.x <= self.x_bound[0] or self.hero.rect.x >= self.x_bound[1]\
                or self.hero.rect.y <= self.y_bound[0] or self.hero.rect.y >= self.y_bound[1]:
            self.hero.rect.x = random.randint(self.x_bound[0], self.x_bound[1])
            self.hero.rect.y = random.randint(self.y_bound[0], self.y_bound[1])

    def check_princess_outbound(self):
        # like hero's
        if self.princess.rect.x <= self.x_bound[0] or self.princess.rect.x >= self.x_bound[1]\
                or self.princess.rect.y <= self.y_bound[0] or self.princess.rect.y >= self.y_bound[1]:
            self.princess.rect.x = random.randint(self.x_bound[0], self.x_bound[1])
            self.princess.rect.y = random.randint(self.y_bound[0], self.y_bound[1])


    def random_appear(self):
        # let the functional sprite appear in a fixed rate, and put them into a list and a group, in list,we can randomly choose one to destroy,in group, we can manage them easily.
        if self.func_intv == 0:
            self.func_intv = self.func_intv_constant
            new_functional_spr_idx = random.choice([1, 2, 3, 4, 5, 6, 7,8,9,10,11,12,13,14,15,16,17])
            new_functional_spr = pygame.sprite.Sprite()
            new_functional_spr.image = self.func_spr_img[new_functional_spr_idx]
            new_functional_spr.rect = new_functional_spr.image.get_rect()
            new_functional_spr.idx = new_functional_spr_idx
            new_functional_spr.rect.x = random.randint(self.x_bound[0], self.x_bound[1])
            new_functional_spr.rect.y = random.randint(self.y_bound[0], self.y_bound[1])
            self.func_group.add(new_functional_spr)
            self.func_spr_lst.append(new_functional_spr)
            if len(self.func_spr_lst) >= self.max_functional_sprite:
                destroy_spr = self.func_spr_lst.pop(random.randint(0, len(self.func_spr_lst)-1))
                destroy_spr.remove(self.func_group)

        else:
            self.func_intv -= 1


    def replace_hana(self):
        for spr in self.func_group:
            spr.image = self.func_spr_img[7]

    def replace_hana_recover(self):
        for spr in self.func_group:
            spr.image = self.func_spr_img[spr.idx]





    def collide_hook(self, player, functional_spr):
        # call when player touch something.
        print('COLLIDE:{}'.format(functional_spr.idx))

        if 'fragrant_flower' in self.big_cache and self.big_cache['fragrant_flower']:
            choice = random.choice([0, 1, 2])
            if choice == 0:
                self.function_count['hero']['red_hana']['count'] += 1
                self.function_count['hero']['red_hana']['timer'] = self.hana_disappear_timer
            elif choice == 1:
                self.function_count['hero']['yellow_hana']['count'] += 1
                self.function_count['hero']['yellow_hana']['timer'] = self.hana_disappear_timer
            elif choice == 2:
                self.function_count['hero']['blue_hana']['count'] += 1
                self.function_count['hero']['blue_hana']['timer'] = self.hana_disappear_timer
            self.play_sound_effect('beep2')
            return






        if functional_spr.idx != 6:
            self.play_sound_effect('beep1')

        if player.name == 'hero':
            if functional_spr.idx == 6 and self.hero.can_boom:
                # instance a new boom and add it to the effect lst.
                boom = pygame.sprite.Sprite()
                boom.image = self.func_spr_img[0]
                boom.pause = self.fixed_time
                boom.rect = self.func_spr_img[0].get_rect()
                boom.rect.x, boom.rect.y = functional_spr.rect.x, functional_spr.rect.y
                self.effect_group.add(boom)
                self.effect_group_lst.append(boom)

                # update hero's status
                self.hero.can_update = False
                self.hero.image = self.hero_img[4]
                self.hero.rect = self.hero_img[4].get_rect()
                self.hero.pause = self.fixed_time

                # print(functional_spr)
                player.life -= 1
                self.fresh_all_functional_count_hero()
                self.just_update_screen()
                self.hero.can_magic = True
                # time.sleep(2)

                self.play_sound_effect('boom')

                self.hero.super_fast = False


            # three flowers
            elif functional_spr.idx == 7:
                self.function_count['hero']['red_hana']['count'] += 1
                self.function_count['hero']['red_hana']['timer'] = self.hana_disappear_timer

            elif functional_spr.idx == 2:
                self.function_count['hero']['yellow_hana']['count'] += 1
                self.function_count['hero']['yellow_hana']['timer'] = self.hana_disappear_timer

            elif functional_spr.idx == 3:
                self.function_count['hero']['blue_hana']['count'] += 1
                self.function_count['hero']['blue_hana']['timer'] = self.hana_disappear_timer

            # kokoro - add life
            elif functional_spr.idx == 1:
                self.hero.life += 1
                self.function_count['hero']['kokoro'] += 1

            elif functional_spr.idx == 4:
                # fragrant
                self.function_count['hero']['fragrant'] += 1
                self.big_cache['fragrant_flower'] = True
                self.big_cache['fragrant_flower_count'] = 200
                self.replace_hana()



            elif functional_spr.idx == 5:
                self.function_count['hero']['cake'] += 1

            elif functional_spr.idx == 16:
                # self.stop_play_sound()
                # self.play_sound_effect('rain')
                # self.play_bgm('crystal')
                # self.screen_color = (152, 161, 216)
                # self.screen.fill(self.screen_color)
                pass

            # star
            elif functional_spr.idx == 8:
                if self.hero.can_boom:
                    self.hero.can_boom = False
                else:
                    self.hero.can_boom = True


            elif functional_spr.idx == 12:
                if not self.hero.super_fast:
                    self.hero.super_fast = True
                    self.big_cache['hero_origin_can_boom'] = self.hero.can_boom
                    self.hero.can_boom = True
                    if self.hero.super_fast:
                        self.big_cache['super_fast_count_hero'] = 1200
                else:
                    self.hero.super_fast = False
                    self.hero.can_boom = self.big_cache['hero_origin_can_boom']


            # pen
            elif functional_spr.idx == 17:
                # print('here')
                if not self.big_cache['boom_lock']:
                    self.big_cache['boom_lock'] = True
                    self.big_cache['boom_rain'] = True
                    # print('here')
                    x_range = [i for i in range(self.w)]
                    # y_range = [i for i in range(self.h)]
                    v_range = [10, 20, 30, -10, -20, -30]
                    self.big_cache['boom_sprite_lst'] = []
                    self.big_cache['delete_boom'] = 0
                    self.big_cache['boom_lock_count'] = 600
                    for count in range(self.big_cache['boom_quantity']):
                        boom_sprite = pygame.sprite.Sprite()
                        boom_sprite.image = self.func_spr_img[6]
                        boom_sprite.rect = self.func_spr_img[6].get_rect()
                        boom_sprite.rect.x = random.choice(x_range)
                        boom_sprite.rect.y = 0
                        boom_sprite.idx = 6
                        boom_sprite.idx_2 = count
                        boom_sprite.name = 'boom_rain'
                        boom_sprite.v_x = random.choice(v_range)
                        boom_sprite.v_y = random.choice(v_range)
                        # self.big_cache['boom_sprite_dct'].add(boom_sprite)
                        self.func_group.add(boom_sprite)
                        self.func_spr_lst.append(boom_sprite)
                        self.big_cache['delete_boom'] += 1


                        # self.big_cache['boom_sprite_lst'].append(boom_sprite)

                    # print('ph1', [i.idx for i in self.func_spr_lst])


                else:
                    return


            else:
                self.function_count['hero'][self.idx_spr_dct[functional_spr.idx]] += 1







        elif player.name == 'princess':
            # todo:add logic that princess touches the bomb
            if functional_spr.idx == 6 and self.princess.can_boom:
                boom = pygame.sprite.Sprite()
                boom.image = self.func_spr_img[0]
                boom.pause = self.fixed_time
                boom.rect = self.func_spr_img[0].get_rect()
                boom.rect.x, boom.rect.y = functional_spr.rect.x, functional_spr.rect.y
                self.effect_group.add(boom)
                self.effect_group_lst.append(boom)

                # update princess's status
                self.princess.can_update = False
                self.princess.image = self.princess_img[4]
                self.princess.rect = self.princess_img[4].get_rect()
                self.princess.pause = self.fixed_time

                self.fresh_all_functional_count_princess()

                # print(functional_spr)
                # player.life -= 1
                self.just_update_screen()

                self.play_sound_effect('boom')

                self.princess.super_fast = False

            # when touch cake, fresh timer
            elif functional_spr.idx == 5:
                self.function_count['princess']['cake'] += 1
                self.big_cache['timer'] = 99


            elif functional_spr.idx == 9: # 11 14
                self.function_count['princess']['tree'] += 1
            elif functional_spr.idx == 11:
                self.function_count['princess']['carrot'] += 1
            elif functional_spr.idx == 14:
                self.big_cache['timer_dec'] += 2000
                self.function_count['princess']['fish'] += 1


            # pinao
            elif functional_spr.idx == 16:
                self.stop_play_sound()
                self.play_sound_effect('rain')
                self.play_bgm('crystal')
                self.screen_color = (152, 161, 216)
                # self.screen.fill(self.screen_color)
                self.big_cache['update_timer'] = not self.big_cache['update_timer']

            # star
            elif functional_spr.idx == 8:
                if self.princess.can_boom:
                    self.princess.can_boom = False
                else:
                    self.princess.can_boom = True

            # heel
            elif functional_spr.idx == 12:
                # self.move_intv_princess = 50 if self.move_intv_princess < 50 else self.move_intv_origin
                self.princess.super_fast = not self.princess.super_fast
                if self.princess.super_fast:
                    self.big_cache['super_fast_count_princess'] = 1200

            # moon
            elif functional_spr.idx == 10:
                if not self.big_cache['moon']:
                    self.big_cache['moon'] = True
                    self.hana_disappear_timer = 6000
                else:
                    self.big_cache['moon'] = False
                    self.hana_disappear_timer = 600

            # pen
            elif functional_spr.idx == 17:
                # print('here')
                if not self.big_cache['boom_lock']:
                    self.big_cache['boom_lock'] = True
                    self.big_cache['boom_rain'] = True
                    # print('here')
                    x_range = [i for i in range(self.w)]
                    # y_range = [i for i in range(self.h)]
                    v_range = [10, 20, 30, -10, -20, -30]
                    self.big_cache['boom_sprite_lst'] = []
                    self.big_cache['delete_boom'] = 0
                    self.big_cache['boom_lock_count'] = 600
                    for count in range(self.big_cache['boom_quantity']):
                        boom_sprite = pygame.sprite.Sprite()
                        boom_sprite.image = self.func_spr_img[6]
                        boom_sprite.rect = self.func_spr_img[6].get_rect()
                        boom_sprite.rect.x = random.choice(x_range)
                        boom_sprite.rect.y = 0
                        boom_sprite.idx = 6
                        boom_sprite.idx_2 = count
                        boom_sprite.name = 'boom_rain'
                        boom_sprite.v_x = random.choice(v_range)
                        boom_sprite.v_y = random.choice(v_range)
                        # self.big_cache['boom_sprite_dct'].add(boom_sprite)
                        self.func_group.add(boom_sprite)
                        self.func_spr_lst.append(boom_sprite)
                        self.big_cache['delete_boom'] += 1

                        # self.big_cache['boom_sprite_lst'].append(boom_sprite)

                    # print('ph1', [i.idx for i in self.func_spr_lst])


                else:
                    return

            else:
                try:
                    self.function_count['princess'][self.idx_spr_dct[functional_spr.idx]] += 1
                except:
                    pass



    def fresh_all_functional_count_hero(self):
        # when hero touch bomb

        self.function_count['hero'] = {'red_hana': {'count': 0, 'timer': 0},
                                        'blue_hana': {'count': 0, 'timer': 0},
                                        'yellow_hana': {'count': 0, 'timer': 0},
                                        'fragrant': 0,
                                        'cake': 0,
                                        'star': 0,
                                        'tree': 0,
                                        'moon': 0,
                                        'carrot': 0,
                                        'heel': 0,
                                        'wine': 0,
                                        'fish': 0,
                                        'candle': 0,
                                        'piano': 0,
                                        'pen': 0,
                                        'kokoro':0,
                                        'bomb': 0,
                                        }

    def fresh_all_functional_count_princess(self):
        # when princess touch bomb

        self.function_count['princess'] = {'red_hana': {'count': 0, 'timer': 0},
                                       'blue_hana': {'count': 0, 'timer': 0},
                                       'yellow_hana': {'count': 0, 'timer': 0},
                                       'fragrant': 0,
                                       'cake': 0,
                                       'star': 0,
                                       'tree': 0,
                                       'moon': 0,
                                       'carrot': 0,
                                       'heel': 0,
                                       'wine': 0,
                                       'fish': 0,
                                       'candle': 0,
                                       'piano': 0,
                                       'pen': 0,
                                       'kokoro':0,
                                       'bomb':0,
                                       }



    def update_information(self):
        # according to backend data, update information to display and player features.

        # boom_rain
        # print(self.big_cache['boom_rain'])
        # print(self.big_cache['boom_lock'])
        # if 'delete_boom' in self.big_cache:
        #     print('del', self.big_cache['delete_boom'])

        if 'boom_rain' in self.big_cache and self.big_cache['boom_rain']:
            self.big_cache['boom_lock_count'] -= 1
            if self.big_cache['boom_lock_count'] <= 0:
                self.big_cache['boom_rain'] = False
                self.big_cache['boom_lock'] = False
                self.big_cache['delete_boom'] = 0
            # print('bmr_here1')
            temp_func_spr_lst = []
            # if not 'delete_boom' in self.big_cache:
            #     self.big_cache['delete_boom'] = self.big_cache['boom_quantity']
            # print([i.idx for i in self.func_spr_lst])
            for spr in self.func_spr_lst:
                if spr.idx == 6:
                    # print('hasattr',  hasattr(spr, 'name'))
                    if hasattr(spr, 'name'):
                        # print('hasattr')
                        if spr.name == 'boom_rain':
                            spr.rect.x += spr.v_x
                            spr.rect.y += spr.v_y
                            # print('bmr_here2')
                            if spr.rect.x < 0 - 20 or  spr.rect.x > self.w + 20 or spr.rect.y > self.h + 20 or spr.rect.y < 0 - 20:
                                self.func_group.remove(spr)
                                # print('remove 1!')
                                self.big_cache['delete_boom'] -= 1
                                if self.big_cache['delete_boom'] <= 0:
                                    self.big_cache['boom_rain'] = False
                                    self.big_cache['boom_lock'] = False
                                    # del self.big_cache['delete_boom']
                            else:
                                temp_func_spr_lst.append(spr)
                            pass
                        else:
                            temp_func_spr_lst.append(spr)
                    else:
                        temp_func_spr_lst.append(spr)
                else:
                    temp_func_spr_lst.append(spr)
            self.func_spr_lst = temp_func_spr_lst



        if 'fragrant_flower' in self.big_cache and self.big_cache['fragrant_flower']:
            if self.big_cache['fragrant_flower_count'] - 1 > 0:
                self.big_cache['fragrant_flower_count'] -= 1
            else:
                self.big_cache['fragrant_flower'] = False
                del self.big_cache['fragrant_flower_count']
                self.replace_hana_recover()


        # update timer
        if self.big_cache['update_timer']:
            if self.big_cache['timer_dec'] - 1 > 0:
                self.big_cache['timer_dec'] -= 1
            else:
                self.big_cache['timer_dec'] = self.timer_intv
                if self.big_cache['timer'] - 1 == 0:
                    self.stop_play_sound()
                    self.game_over()
                else:
                    self.big_cache['timer'] -= 1
            if len(str(self.big_cache['timer'])) == 2:
                self.timer_shi.image = self.num_img_lst[int(str(self.big_cache['timer'])[0])]

                self.timer_ge.image = self.num_img_lst[int(str(self.big_cache['timer'])[1])]
            else:
                self.timer_shi.image = self.num_img_lst[0]
                self.timer_ge.image = self.num_img_lst[int(str(self.big_cache['timer'])[0])]


        # for hero

        # red hana count update
        if self.function_count['hero']['red_hana']['count'] > 0:
            self.function_count['hero']['red_hana']['timer'] -= 1
            if self.function_count['hero']['red_hana']['timer'] == 0:
                self.function_count['hero']['red_hana']['count'] -= 1
                if self.function_count['hero']['red_hana']['count'] > 0:
                    self.function_count['hero']['red_hana']['timer'] = self.hana_disappear_timer
        self.information_spr_dict['hero_red_hana_count'].image = self.num_img_lst[
            self.function_count['hero']['red_hana']['count'] if self.function_count['hero']['red_hana']['count'] < 9 else 10
        ]

        # yellow hana count update
        if self.function_count['hero']['yellow_hana']['count'] > 0:
            self.function_count['hero']['yellow_hana']['timer'] -= 1
            if self.function_count['hero']['yellow_hana']['timer'] == 0:
                self.function_count['hero']['yellow_hana']['count'] -= 1
                if self.function_count['hero']['yellow_hana']['count'] > 0:
                    self.function_count['hero']['yellow_hana']['timer'] = self.hana_disappear_timer
        self.information_spr_dict['hero_yellow_hana_count'].image = self.num_img_lst[
            self.function_count['hero']['yellow_hana']['count'] if self.function_count['hero']['yellow_hana']['count'] <= 9 else 10
        ]

        # blue hana count update
        if self.function_count['hero']['blue_hana']['count'] > 0:
            self.function_count['hero']['blue_hana']['timer'] -= 1
            if self.function_count['hero']['blue_hana']['timer'] == 0:
                self.function_count['hero']['blue_hana']['count'] -= 1
                if self.function_count['hero']['blue_hana']['count'] > 0:
                    self.function_count['hero']['blue_hana']['timer'] = self.hana_disappear_timer
        self.information_spr_dict['hero_blue_hana_count'].image = self.num_img_lst[
            self.function_count['hero']['blue_hana']['count'] if self.function_count['hero']['blue_hana']['count'] <= 9 else 10
        ]

        # kokoro count update
        self.information_spr_dict['hero_kokoro_count'].image = self.num_img_lst[
            self.hero.life if self.hero.life <= 9 else 10
        ]

        # judge life time
        if self.hero.life == 0:
            self.stop_play_sound()
            self.game_over()

        # uodate hero's speed
        if self.hero.super_fast:
            self.big_cache['super_fast_count_hero'] -= 1
            if self.big_cache['super_fast_count_hero'] <= 0:
                self.hero.super_fast = False


        if self.hero.super_fast:
            self.move_intv = 60
        else:
            # self.move_intv = self.move_intv_origin + self.function_count['hero']['fragrant']
            self.move_intv = self.move_intv_origin + self.function_count['princess']['fish'] * 10 - self.function_count['hero']['wine'] * 5
            if self.move_intv <= 0:
                self.move_intv = 3

        # update princess's speed
        if self.princess.super_fast:
            self.big_cache['super_fast_count_princess'] -= 1
            if self.big_cache['super_fast_count_princess'] <= 0:
                self.princess.super_fast = False


        if self.princess.super_fast:
            self.move_intv_princess = 60
        else:
            # self.move_intv = self.move_intv_origin + self.function_count['hero']['fragrant']
            self.move_intv_princess = self.move_intv_origin + self.function_count['princess']['carrot'] * 10 - self.function_count['princess']['wine'] * 5
            if self.move_intv_princess <= 0:
                self.move_intv_princess = 3

        # update key info cake and candle img
        if self.function_count['hero']['cake'] > 0:
            self.information_spr_dict['hero_cake'].image = self.information_cake_image
        if self.function_count['hero']['cake'] == 0:
            self.information_spr_dict['hero_cake'].image = self.information_blank_image

        if self.function_count['hero']['candle'] > 0:
            self.information_spr_dict['hero_fragrant'].image = self.information_fragrant_image
        if self.function_count['hero']['candle'] == 0:
            self.information_spr_dict['hero_fragrant'].image = self.information_blank_image

        # judge if hero meets the requirement
        if self.function_count['hero']['red_hana']['count'] >= self.require_hana and\
            self.function_count['hero']['yellow_hana']['count'] >= self.require_hana and\
            self.function_count['hero']['blue_hana']['count'] >= self.require_hana and \
            self.function_count['hero']['candle'] >= 1 and \
            self.function_count['hero']['cake'] >= 1:
            self.hero.can_chase_princess = True
        else:
            self.hero.can_chase_princess = False

        # self.move_intv = self.move_intv_origin + self.function_count['hero']['fragrant']
        # self.move_intv_princess = self.move_intv_origin + self.function_count['hero']['cake']

        # for princess
        # update carrot count
        self.information_spr_dict['princess_carrot_count'].image = self.num_img_lst[
            self.function_count['princess']['carrot'] if self.function_count['princess']['carrot'] <= 9 else 10
        ]
        # self.move_intv_princess = self.move_intv_origin + self.function_count['princess']['carrot'] * 10

        # update fish count
        self.information_spr_dict['princess_fish_count'].image = self.num_img_lst[
            self.function_count['princess']['fish'] if self.function_count['princess']['fish'] <= 9 else 10
        ]
        # update in the former part

        # update tree count
        self.information_spr_dict['princess_tree_count'].image = self.num_img_lst[
            self.function_count['princess']['tree'] if self.function_count['princess']['tree'] <= 9 else 10
        ]
        # inc timer intv
        self.timer_intv = 200 + self.function_count['princess']['tree'] * 10

        # update moon display
        if self.big_cache['moon']:
            self.information_spr_dict['princess_moon'].image = self.display_moon
        else:
            self.information_spr_dict['princess_moon'].image = self.blank_moon




        # for hero, if can chase, display signal
        if self.hero.can_chase_princess:
            self.can_chase_note.image = self.can_chase_kokoro_img
            # self.can_chase_note.rect = self.can_chase_kokoro_img.get_rect()
            # self.can_chase_note.rect.x = 10
            # self.can_chase_note.rect.y = 600

            # print('can')
        else:
            self.can_chase_note.image = self.blank_img
            # self.can_chase_note.rect = self.blank_img.get_rect()
            # self.can_chase_note.rect.x = 10
            # self.can_chase_note.rect.y = 600
            # print('cannot')




    def just_update_screen(self):
        # update display every loop
        self.init_screen()
        self.func_group.draw(self.screen)
        self.effect_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.information_group.draw(self.screen)
        pygame.display.update()

    def functional_update(self):
        # update effect,functional object, player status every loop
        self.check_hero_outbound()
        self.check_princess_outbound()
        self.functional_update_hero()
        self.functional_update_princess()
        self.update_effect()
        self.random_appear()
        self.update_information()


    def run(self):
        self.play_bgm(self.curr_bgm)


        while True:
            # detect key event for hero and princess
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    keys = list(pygame.key.get_pressed())
                    # print(keys[44], keys[26], keys[22], keys[4], keys[7])
                    # print(keys.index(True))

                    # for hero
                    # blank
                    if self.hero.can_update:
                        if keys[44]:
                            # self.update_hero()
                            # self.hero.rect.y += self.move_intv
                            self.update_hero_magic()



                        # up
                        if keys[26]:
                            self.update_hero()
                            self.hero.rect.y -= self.move_intv
                        # down
                        if keys[22]:
                            self.update_hero()
                            self.hero.rect.y += self.move_intv
                        # left
                        if keys[4]:
                            self.update_hero()
                            self.hero.rect.x -= self.move_intv
                        # right
                        if keys[7]:
                            self.update_hero()
                            self.hero.rect.x += self.move_intv

                    if self.princess.can_update:
                    # for princess
                    # up
                        if keys[82]:
                            self.update_princess()
                            self.princess.rect.y -= self.move_intv_princess
                        # down
                        if keys[81]:
                            self.update_princess()
                            self.princess.rect.y += self.move_intv_princess

                        # left
                        if keys[80]:
                            self.update_princess()
                            self.princess.rect.x -= self.move_intv_princess

                        # right
                        if keys[79]:
                            self.update_princess()
                            self.princess.rect.x += self.move_intv_princess

            # detect collide between functional sprite and players
            count = 0
            delete_lst = []
            for spr in self.func_spr_lst:
                # for hero
                res = pygame.sprite.collide_rect_ratio(0.9)(self.hero, spr)
                if res:
                    # spr.rect.x = -100
                    # spr.rect.y = -100
                    self.collide_hook(self.hero, spr)
                    spr.remove(self.func_group)
                    delete_lst.append(count)

                else:
                    res = pygame.sprite.collide_rect_ratio(0.9)(self.princess, spr)
                    if res:
                        self.collide_hook(self.princess, spr)
                        spr.remove(self.func_group)
                        delete_lst.append(count)

                count += 1
            temp_func_spr_lst = []
            if delete_lst:
                for idx in range(len(self.func_spr_lst)):
                    if idx in delete_lst:
                        continue
                    temp_func_spr_lst.append(self.func_spr_lst[idx])
                self.func_spr_lst = temp_func_spr_lst


            # if condition's reach, detect hero and princess collide
            if self.hero.can_chase_princess:
                res = pygame.sprite.collide_rect_ratio(0.9)(self.hero, self.princess)
                if res:
                    self.play_sound_effect('beep3')
                    self.game_success()
                    self.stop_play_sound()
                    return True

            # finally, judge exit flag
            if self.exit_flag:
                self.stop_play_sound()
                return False

            # finally, do it in every loop.
            self.functional_update()
            # self.screen.fill((255, 255, 255))
            self.just_update_screen()
            # self.hero.rect.h -= 1

    def game_over(self):
        self.play_sound_effect('fail')
        self.exit_flag = True
        pygame.key.set_repeat(0)
        print('游戏结束！')

    def game_success(self):
        print('成功！')

    def game_next_scene(self, display_player=0):
        mask_img = pygame.Surface([1024, 1024])
        mask_img.fill((255, 255, 255))
        self.screen.blit(mask_img, (0, 0))
        for r in range(255, 0, -1):
            mask_img.fill((r, r, r))
            self.screen.blit(mask_img, (0, 0))
            pygame.time.delay(3)
            pygame.display.update()
        game_next = self.load_image('assets/next.PNG', (768, 768))

        game_level = self.load_image('assets/{}.PNG'.format(self.require_hana+4), (150, 150))

        self.play_bgm('hiden_bgm')

        player_group = pygame.sprite.Group()

        if display_player == 0:
            player_img = self.load_image('assets/smile.png', (150, 150))
        else:
            player_img = self.load_image('assets/_happy2.png', (150, 150))
        player = pygame.sprite.Sprite()
        player.image = player_img
        player.rect = player_img.get_rect()
        player.rect.x = 700
        player.rect.y = 300
        player_group.add(player)

        update_count = 5




        while True:
            self.screen.blit(mask_img, (0, 0))
            self.screen.blit(game_next, (100, 0))
            self.screen.blit(game_level, (100, 500))

            if update_count > 0:
                update_count -= 1
                player.rect.y -= 1
            else:
                update_count = 5
                player.rect.y = 300
            player_group.draw(self.screen)
            pygame.display.update()



            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    keys = list(pygame.key.get_pressed())
                    if keys[44]:
                        return
        pass


    def game_over_scene(self):
        # self.init_screen()
        self.play_sound_effect('fail')
        mask_img = pygame.Surface([1024, 1024])
        mask_img.fill((255,255,255))
        self.screen.blit(mask_img, (0,0))
        for r in range(255, 0, -1):
            mask_img.fill((r,r,r))
            self.screen.blit(mask_img, (0, 0))
            pygame.time.delay(3)
            pygame.display.update()
        game_over_img = self.load_image('assets/game_over.PNG', (1024, 1024))

        hero_die_image = self.load_image('assets/_die.PNG', (200, 200))

        princess_die_image = self.load_image('assets/die.PNG', (200, 200))

        while True:
            self.screen.blit(game_over_img, (-30, -170))
            self.screen.blit(hero_die_image, (200, 450))
            self.screen.blit(princess_die_image, (500, 450))


            pygame.display.update()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    keys = list(pygame.key.get_pressed())
                    if keys[44]:
                        return

    def game_success_scene(self):
        # when pass 9 level, display the movie.
        # movie = pygame.movie.Movie('assets/ending.m4v')
        self.play_bgm('happy_birthday_on_f')
        pygame.key.set_repeat(0,0)
        clip = VideoFileClip('assets/ending.m4v')
        # movie.set_display(self.screen)
        # movie.play()
        clip.preview()

        end_scene_lst = [
            'end3',
            'end4',
            'end1',
            'end2',
            'end5',
            'end7'
        ]
        self.screen.fill((0,0,0))
        for end in end_scene_lst:


            img = self.load_image('assets/{}.PNG'.format(end), (768, 768))
            self.screen.blit(img, (50,0))

            flag = False
            while True:
                # self.screen.blit(mask_img, (0, 0))
                # self.screen.blit(game_next, (100, 0))
                # self.screen.blit(game_level, (100, 500))
                if flag:
                    break

                pygame.display.update()
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        keys = list(pygame.key.get_pressed())
                        if keys[44]:
                            flag = True
                            break

        self.stop_play_sound()


    def hello_scene(self):
        # hello scene
        self.play_bgm('merryChristmasOnbE')

        mask_img = pygame.Surface([1024, 1024])
        mask_img.fill((0,0,0))
        self.screen.blit(mask_img, (0,0))
        for r in range(0, 255, 1):
            mask_img.fill((r,r,r))
            self.screen.blit(mask_img, (0, 0))
            pygame.time.delay(3)
            pygame.display.update()
        game_hello_img_enter = self.load_image('assets/hello_start.PNG', (764, 764))
        game_hello_img_quit = self.load_image('assets/hello_quit.PNG', (764, 764))

        now_choose = 0

        hero_img = self.load_image('assets/_main.PNG', (150, 150))
        princess_img = self.load_image('assets/main.PNG', (150, 150))



        position = (100,0)

        while True:
            self.init_screen()

            if now_choose == 0:
                self.screen.blit(game_hello_img_enter, position)
            elif now_choose == 1:
                self.screen.blit(game_hello_img_quit, position)
            # hello menu with 2 item 0 or 1
            self.screen.blit(princess_img, (800, 180))
            self.screen.blit(hero_img, (50, 150))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = list(pygame.key.get_pressed())
                    if keys[44]:
                        if now_choose == 0:
                            pygame.key.set_repeat(40, 40)  # hold key interval
                            self.stop_play_sound()
                            self.play_sound_effect('choose')
                            return 0
                        elif now_choose == 1:
                            self.play_sound_effect('choose')
                            self.stop_play_sound()
                            return 1
                    if keys[81]:
                        # down
                        self.play_sound_effect('switch')
                        if now_choose == 0:
                            now_choose = 1
                        elif now_choose == 1:
                            now_choose = 0

                    if keys[82]:
                        # up
                        self.play_sound_effect('switch')
                        if now_choose == 0:
                            now_choose = 1
                        elif now_choose == 1:
                            now_choose = 0

        pass


class Master:

    def __init__(self):
        self.level_config_dct = {1:
                                     {'b':'lonely_chase', 'c':(231,249,207)},
                                 5:
                                     {'b':'aki_legend', 'c':(224,235,244)},
                                 9:
                                     {'b':'AkiNoHanashionDmajor', 'c':(0,0,0)}
        }




    def game_manager(self):

        ORIGIN_HERO_KOKORO = 3

        MAX_LEVEL = 9
        curr_hero_kokoro = ORIGIN_HERO_KOKORO
        level = 1



        while True:
            game = scene1(screen_color=self.level_config_dct[level]['c'], hero_kokoro=curr_hero_kokoro, curr_bgm=self.level_config_dct[level]['b'])
            user_choose = game.hello_scene()
            if user_choose == 0:
                while game.run():
                    # if enter that means win
                    # first, display next scene
                    # then, level up
                    if level >= MAX_LEVEL:
                        game.game_success_scene()
                        curr_hero_kokoro = ORIGIN_HERO_KOKORO
                        level = 1


                        break
                    # then, init all parameters
                    game.game_next_scene()
                    level += 4
                    curr_hero_kokoro = game.hero.life
                    game.__init__(level, hero_kokoro=curr_hero_kokoro, screen_color=self.level_config_dct[level]['c'], curr_bgm=self.level_config_dct[level]['b'])



                    # print(sys.getsizeof(game))
                else:
                    # if enter that means fail
                    game.game_over_scene()
                    curr_hero_kokoro = ORIGIN_HERO_KOKORO
                    level = 1
            elif user_choose == 1:
                pygame.display.quit()
                quit()
            del game
            # level += 1





    def run(self):
        self.game_manager()

    def test(self):
        # game = scene1()
        # game.just_update_screen()
        # game.hello_scene()
        while True:
            game = scene1()
            # game.game_over_scene()
            # game.game_next_scene(display_player=1)
            game.game_success_scene()


        # while True:
        #     game.just_update_screen()
        #     game.init_screen()





if __name__ == '__main__':

    # s1 = scene1()
    m = Master()
    m.run()
    # m.test()
    #234