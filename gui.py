import threading
import time

import PySimpleGUI as sg
import controls


def run_gui():
    def buff_timer(
            buff_timer_default=None,
            key_string=None,
            buff_string=None,
            window=None
    ):
        buff_timer = buff_timer_default
        buff_timer_display = 0
        buff_timer_isRunning = False

        while True:
            start_time = time.time()

            if controls.look_for_buffs("nullify") is not None:
                # Nullify -> Buff
                buff_timer_isRunning = False
                buff_timer = 0
                buff_timer_display = int(buff_timer)
                # Send event to the main thread to update the GUI
                window.write_event_value(key_string, buff_timer_display)
                buff_timer = buff_timer_default

            if controls.look_for_buffs(buff_string) is not None:
                buff_timer_isRunning = True

            if buff_timer_isRunning is True:
                buff_timer = max(buff_timer - 1, 0)  # decrease timer by 1, but ensure it is not negative
                buff_timer_display = int(buff_timer)
                window.write_event_value(key_string, buff_timer_display)
                if buff_timer == 0:
                    buff_timer_isRunning = False
                    buff_timer = buff_timer_default

            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)

            if stop_checking_for_buffs.is_set():
                break

    def update_cerebral_thought_timer(window):
        buff_timer(
            buff_timer_default=7200,
            key_string='-CerebralThoughtTimer-',
            buff_string='cerebral_thought',
            window=window
        )

    def update_jandros_timer(window):
        buff_timer(
            buff_timer_default=600,
            key_string='-JandrosTimer-',
            buff_string='jandros',
            window=window
        )

    def update_mysticward_timer(window):
        buff_timer(
            buff_timer_default=240,
            key_string='-WardTimer-',
            buff_string='ward',
            window=window
        )

    def run_runechecker(window):
        while not stop_runechecker.is_set():
            # Variable to be set every time the window is refreshed
            runes_need_refreshing = True
            key_value = '-RuneStateImage-'
            ok_image = 'images/OK.png'
            replace_image = 'images/REPLACE.gif'

            if controls.rune_checker() is False and runes_need_refreshing is False:
                if runes_need_refreshing is False:
                    window.write_event_value(key_value, ok_image)
                else:
                    window.write_event_value(key_value, replace_image)
            if controls.rune_checker() is True:
                runes_need_refreshing = True
                window.write_event_value(key_value, replace_image)
            if controls.check_if_rune_was_refreshed() is not None:
                runes_need_refreshing = False
                window.write_event_value(key_value, ok_image)

    def run_autoskinner(stop_event=None):
        while True:
            controls.corpse_check()
            if stop_event is not None and stop_event.is_set():
                break

    def run_autobuffer(window):
        key_value = '-Autobuffer-'
        while True:
            controls.auto_buff(stop_autobuff_flag)
            window.write_event_value(key_value, False)
            if not run_autobuff_flag:
                break
            time.sleep(0.1)  # add a short sleep to reduce CPU usage

    def run_autohunter(window):
        key_value = '-Autohunter-'
        while True:
            controls.auto_hunt(stop_autohunt_flag)
            window.write_event_value(key_value, False)
            if not run_autohunt_flag:
                window['-Down-'].update(disabled=False)
                window['-Up-'].update(disabled=False)
                window['-Left-'].update(disabled=False)
                window['-Right-'].update(disabled=False)
                if window['-Down-'].get():
                    window['-Down-'].update(value=False)
                if window['-Up-'].get():
                    window['-Up-'].update(value=False)
                if window['-Left-'].get():
                    window['-Left-'].update(value=False)
                if window['-Right-'].get():
                    window['-Right-'].update(value=False)
                controls.up = False
                controls.down = False
                controls.left = False
                controls.right = False
                break
            time.sleep(0.1)

    sg.theme('Dark')  # Add a touch of color
    # All the stuff inside the window.
    layout = \
        [
            [sg.Text(" ")],
            [sg.Text('Rune status'), sg.Image(filename='images/OK.png', enable_events=True, key='-RuneStateImage-')],
            [sg.Text(" ")],
            [sg.Text('Mage Buffs'), sg.Text('Time remaining:'),
             sg.Text(" ", size=(10, 1), key='-CerebralThoughtTimer-')],
            [sg.Text(" ")],
            [sg.Text('Jandros Oil'), sg.Text('Time remaining:'),
             sg.Text(" ", size=(10, 1), key='-JandrosTimer-')],
            [sg.Text('Mystic Ward'), sg.Text('Time remaining:'),
             sg.Text(" ", size=(10, 1), key='-WardTimer-')],
            [sg.Text(" ")],
            [sg.CBox('Autoskinner', enable_events=True, key='-Autoskinner-')],
            [sg.CBox('Autohunter', enable_events=True, key='-Autohunter-'),
             sg.CBox('Up', enable_events=True, key="-Up-"),
             sg.CBox('Down', enable_events=True, key="-Down-"),
             sg.CBox('Left', enable_events=True, key="-Left-"),
             sg.CBox('Right', enable_events=True, key="-Right-"),
             ],
            [sg.Slider(range=(0, 40), orientation='h', size=(40, 20),
                       change_submits=True, default_value=0, key='-Stepper-')],
            [sg.CBox('Buff me', enable_events=True, key='-Autobuffer-')],
            [sg.Text(" ")],
            [sg.Button('Close')]
        ]

    window = sg.Window('Talazar Tools', layout, finalize=True)

    # Thread handling
    run_autobuff_flag = False  # for auto buffer, if user disable while buffing is happening
    stop_autobuff_flag = threading.Event()  # for auto buffer, if user disable while buffing, for auto_buff()
    run_autohunt_flag = False
    stop_autohunt_flag = threading.Event()
    stop_event = threading.Event()
    stop_runechecker = threading.Event()
    stop_checking_for_buffs = threading.Event()
    runechecker_thread = threading.Thread(target=run_runechecker, args=(window,))
    autoskinner_thread = threading.Thread(target=run_autoskinner, args=(stop_event,))
    autobuffer_thread = threading.Thread(target=run_autobuffer, args=(window,))
    autobuffer_thread.daemon = True
    autohunter_thread = threading.Thread(target=run_autohunter, args=(window,))
    cerebral_thought_timer_thread = threading.Thread(target=update_cerebral_thought_timer, args=(window,))
    jandros_timer_thread = threading.Thread(target=update_jandros_timer, args=(window,))
    mysticward_timer_thread = threading.Thread(target=update_mysticward_timer, args=(window,))

    cerebral_thought_timer_thread.start()
    jandros_timer_thread.start()
    mysticward_timer_thread.start()
    runechecker_thread.start()

    while True:
        event, values = window.read(timeout=100)

        # Handle closing application
        if event == sg.WIN_CLOSED or event == 'Close':
            stop_event.set()
            run_autobuff_flag = False
            stop_autobuff_flag.set()
            stop_autohunt_flag.set()
            stop_runechecker.set()
            stop_checking_for_buffs.set()
            window.close()
            # check for stuck threads
            # time.sleep(1)
            # threads = threading.enumerate()
            # for thread in threads:
            #     print(thread.name)
            break

        elif event == '-CerebralThoughtTimer-':
            window['-CerebralThoughtTimer-'].update(values[event])

        elif event == '-JandrosTimer-':
            window['-JandrosTimer-'].update(values[event])

        elif event == '-WardTimer-':
            window['-WardTimer-'].update(values[event])

        elif event == '-RuneStateImage-':
            window['-RuneStateImage-'].update(values[event])

        elif event == '-Up-':
            if window['-Up-'].get():
                controls.up = True
                controls.down = False
            else:
                controls.up = False
            if window['-Down-']:
                window['-Down-'].update(value=False)
                controls.down = False

        elif event == '-Down-':
            if window['-Down-'].get():
                controls.up = False
                controls.down = True
            else:
                controls.down = False
            if window['-Up-']:
                window['-Up-'].update(value=False)
                controls.up = False

        elif event == '-Left-':
            if window['-Left-'].get():
                controls.left = True
                controls.right = False
            else:
                controls.left = False
            if window['-Right-']:
                window['-Right-'].update(value=False)
                controls.right = False

        elif event == '-Right-':
            if window['-Right-'].get():
                controls.left = False
                controls.right = True
            else:
                controls.right = False
            if window['-Left-']:
                window['-Left-'].update(value=False)
                controls.left = False

        elif event == '-Stepper-':
            controls.step = int(values['-Stepper-'])

        elif event == '-Autobuffer-':
            window['-Autobuffer-'].update(values[event])
            if values[event]:
                run_autobuff_flag = True
                stop_autobuff_flag.clear()
                if not autobuffer_thread.is_alive():
                    autobuffer_thread = threading.Thread(target=run_autobuffer, args=(window,))
                    autobuffer_thread.daemon = True
                    autobuffer_thread.start()
            else:
                run_autobuff_flag = False
                stop_autobuff_flag.set()

        elif event == '-Autohunter-':
            window['-Autohunter-'].update(values[event])
            if values[event]:
                run_autohunt_flag = True
                stop_autohunt_flag.clear()
                window['-Down-'].update(disabled=True)
                window['-Up-'].update(disabled=True)
                window['-Left-'].update(disabled=True)
                window['-Right-'].update(disabled=True)
                if not autohunter_thread.is_alive():
                    autohunter_thread = threading.Thread(target=run_autohunter, args=(window,))
                    autohunter_thread.daemon = True
                    autohunter_thread.start()
            else:
                run_autohunt_flag = False
                stop_autohunt_flag.set()

        if values['-Autoskinner-']:
            if not autoskinner_thread.is_alive():
                stop_event.clear()
                autoskinner_thread = threading.Thread(target=run_autoskinner, args=(stop_event,))
                autoskinner_thread.start()
                controls.autoskinner_running = True
        else:
            if autoskinner_thread.is_alive():
                stop_event.set()
                autoskinner_thread.join()
                controls.autoskinner_running = False

        # if values['-Autobuffer-']:
        #     if not autobuffer_thread.is_alive():
        #         stop_event.clear()
        #         autobuffer_thread = threading.Thread(target=run_autobuffer, args=(window, stop_event,))
        #         autobuffer_thread.start()
        # else:
        #     if autobuffer_thread.is_alive():
        #         stop_event.set()
        #         autobuffer_thread.join()

    window.close()
