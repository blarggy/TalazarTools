import time
import pyautogui

# Defaults

# looks at position x=971 y=775 at a square sized 438x20 pixels from that coordinate (Combat window for buffs)
buff_region = (966, 775, 438, 20)
# looks at position x=1405 y=1212 at a square sized 227x93 pixels from that coordinate (Main system window for chat)
jandros_region = (1405, 1212, 227, 93)
# looks at position x=1551 y=1309 at a square sized 31x33 pixels from that coordinate (Rune Slot Area)
rune_check_region = (1544, 1304, 46, 46)
# the entire region for the game screen
game_region = (965, 394, 1951, 994)
# move mouse to center of game window (eg. the player position)
player_pos = (1823, 687)
# game is old, it needs some time to think...
pause = 0.25

# Images to look for
image_nullify_debuff = 'images/you_cast_nullify_on_yourself.png'
image_cerebral_thought_buff = 'images/you_cast_cerebral_thought_on_yourself.png'
image_resplendence_buff = 'images/you_cast_resplendence.png'
image_grandeur_buff = 'images/you_cast_grandeur.png'
image_malax_buff = 'images/you_cast_malax.png'
image_aegis_buff = 'images/you_cast_aegis.png'
image_darkprayer_buff = 'images/you_cast_darkprayer.png'
image_bulwark_buff = 'images/you_cast_bulwark.png'
image_holyaura_buff = 'images/you_cast_holyaura.png'
image_fortify_buff = 'images/you_cast_fortify.png'
image_jandros_buff = 'images/you_pour_the_oil_of_jandros_on_yourself.png'
image_ward_buff = 'images/you_cast_mystic_ward.png'
image_corpse = 'images/corpse_no_transparency.png'
image_selected_corpse = 'images/selected_corpse_no_transparency.png'

# Buff strings
cerebral_thought_str = "cerebral_thought"
nullify_str = "nullify"
resplendence_str = "resplendence"
grandeur_str = "grandeur"
malax_str = "malax"
aegis_str = "aegis"
darkprayer_str = "darkprayer"
bulwark_str = "bulwarkmight"
holyaura_str = "holyaura"
fortify_str = "fortify"
jandros_str = "jandros"
ward_str = "ward"


def look_for_buffs(buff):
    if buff == cerebral_thought_str:
        check_cerebral_thought = pyautogui.locateOnScreen(image_cerebral_thought_buff, region=buff_region,
                                                          confidence=0.9)
        return check_cerebral_thought
    if buff == nullify_str:
        check_nullify = pyautogui.locateOnScreen(image_nullify_debuff, region=buff_region, confidence=0.9)
        return check_nullify
    if buff == resplendence_str:
        check_resplendence = pyautogui.locateOnScreen(image_resplendence_buff, region=buff_region, confidence=0.9)
        return check_resplendence
    if buff == grandeur_str:
        check_grandeur = pyautogui.locateOnScreen(image_grandeur_buff, region=buff_region, confidence=0.9)
        return check_grandeur
    if buff == malax_str:
        check_malax = pyautogui.locateOnScreen(image_malax_buff, region=buff_region, confidence=0.9)
        return check_malax
    if buff == aegis_str:
        check_aegis = pyautogui.locateOnScreen(image_aegis_buff, region=buff_region, confidence=0.9)
        return check_aegis
    if buff == darkprayer_str:
        check_darkprayer = pyautogui.locateOnScreen(image_darkprayer_buff, region=buff_region, confidence=0.9)
        return check_darkprayer
    if buff == bulwark_str:
        check_bulwark = pyautogui.locateOnScreen(image_bulwark_buff, region=buff_region, confidence=0.9)
        return check_bulwark
    if buff == holyaura_str:
        check_holyaura = pyautogui.locateOnScreen(image_holyaura_buff, region=buff_region, confidence=0.9)
        return check_holyaura
    if buff == fortify_str:
        check_fortify = pyautogui.locateOnScreen(image_fortify_buff, region=buff_region, confidence=0.9)
        return check_fortify
    if buff == jandros_str:
        check_jandros = pyautogui.locateOnScreen(image_jandros_buff, region=jandros_region, confidence=0.9)
        return check_jandros
    if buff == ward_str:
        check_ward = pyautogui.locateOnScreen(image_ward_buff, region=buff_region, confidence=0.9)
        return check_ward


def check_if_rune_was_refreshed():
    refresh_check = pyautogui.locateOnScreen('images/runechecker/malenox_200_charges.png', region=rune_check_region,
                                             confidence=0.9)
    return refresh_check


def rune_checker():
    charges22 = pyautogui.locateOnScreen('images/runechecker/malenox_22_charges.png', region=rune_check_region)
    charges21 = pyautogui.locateOnScreen('images/runechecker/malenox_21_charges.png', region=rune_check_region)
    charges20 = pyautogui.locateOnScreen('images/runechecker/malenox_20_charges.png', region=rune_check_region)

    if charges22 or charges21 or charges20 is not None:
        return True
    else:
        return False


def corpse_check():
    pyautogui.press('space')
    is_corpse = pyautogui.locateAllOnScreen(image_corpse)
    is_selected_corpse = pyautogui.locateAllOnScreen(image_selected_corpse)
    if is_corpse or is_selected_corpse:
        pyautogui.press('u')
        time.sleep(0.25)
        click_corpse = next(is_corpse, None)
        if click_corpse is None:
            click_corpse = next(is_selected_corpse, None)
        if click_corpse is not None:
            pyautogui.click(click_corpse)
            time.sleep(3.5)
            pyautogui.moveTo(996, 419)


def select_rune(fkey):
    time.sleep(0.5)
    pyautogui.keyDown('shift')
    time.sleep(pause)
    pyautogui.press(fkey)
    time.sleep(pause)
    pyautogui.keyUp('shift')
    time.sleep(pause)


def select_buff(fkey):
    pyautogui.keyDown('ctrlleft')
    time.sleep(pause)
    pyautogui.press(fkey)
    time.sleep(pause)
    pyautogui.keyUp('ctrlleft')
    time.sleep(pause)


def cast_buff(spell, stop_flag):
    while True:
        if stop_flag.is_set():
            print('Stopping auto_buff...')
            break

        if look_for_buffs(spell) is not None:
            print(f'{spell} cast...')
            pyautogui.press('esc')
            time.sleep(pause)
            break
        print('clicking!')
        pyautogui.click()
        time.sleep(0.5)


def auto_buff(stop_flag):
    # When called, goes through the process of buffing yourself.
    if stop_flag.is_set():
        return
    time.sleep(1)
    pyautogui.moveTo(player_pos)
    select_rune('f1')  # mind rune
    select_buff("f1")  # nullify
    cast_buff(nullify_str, stop_flag)  # cast nullify
    if stop_flag.is_set():
        return
    select_buff("f2")  # cerebral thought
    cast_buff(cerebral_thought_str, stop_flag)  # cast cerebral thought
    select_buff('f3')  # resplendence
    cast_buff(resplendence_str, stop_flag)  # cast resplendence
    if stop_flag.is_set():
        return
    select_rune('f2')  # nature rune
    select_buff('f4')  # grandeur
    cast_buff(grandeur_str, stop_flag)  # cast grandeur
    if stop_flag.is_set():
        return
    select_rune('f3')  # soul rune
    select_buff('f5')  # malax
    cast_buff(malax_str, stop_flag)  # cast malax
    if stop_flag.is_set():
        return
    select_buff('f6')  # aegis
    cast_buff(aegis_str, stop_flag)  # cast aegis
    if stop_flag.is_set():
        return
    select_buff('f7')  # dark prayer
    cast_buff(darkprayer_str, stop_flag)  # cast dark prayer
    if stop_flag.is_set():
        return
    select_rune('f4')  # body rune
    select_buff('f8')  # bulwark might
    cast_buff(bulwark_str, stop_flag)  # cast bulwark might
    if stop_flag.is_set():
        return
    select_buff('f9')  # holy aura
    cast_buff(holyaura_str, stop_flag)  # cast holy aura
    if stop_flag.is_set():
        return
    select_buff('f10')  # fortify
    cast_buff(fortify_str, stop_flag)  # cast fortify
    if stop_flag.is_set():
        return


def move(keyup=None):
    if up:
        pyautogui.keyDown("w")
        if keyup:
            pyautogui.keyUp("w")
    elif down:
        pyautogui.keyDown("s")
        if keyup:
            pyautogui.keyUp("s")
    if left:
        pyautogui.keyDown("a")
        if keyup:
            pyautogui.keyUp("a")
    elif right:
        pyautogui.keyDown("d")
        if keyup:
            pyautogui.keyUp("d")



def flip_movement():
    global up, down, left, right
    if up:
        up = False
        down = True
    elif down:
        up = True
        down = False
    if left:
        right = True
        left = False
    elif right:
        right = False
        left = True


up = False
down = False
left = False
right = False
step = 0
autoskinner_running = False


def auto_hunt(stop_flag):
    while True:
        step_pause = 1 if not autoskinner_running else 5
        move_speed = 1 if not autoskinner_running else 0.25
        if stop_flag.is_set():
            break
        if step == 0:
            pyautogui.press("`")
            time.sleep(1.5)
        else:
            counter = 0
            while step > counter:
                if stop_flag.is_set():
                    break
                move()
                time.sleep(move_speed)
                move(keyup=True)
                pyautogui.press("`")
                time.sleep(step_pause)
                counter += 1
            if step == counter:
                flip_movement()
                counter = 0


