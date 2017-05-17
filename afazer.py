#! /usr/bin/env python3

# WilliamTODO - Promgrama de TO DO list e tecnica Pomodoro
#
# V.01 - Somenente Pomodoro Simples
#
# Requer:
# Gtk-3 -
# AppIndicator3 -
# Notify -
#  simpleaudio - http://simpleaudio.readthedocs.io
#
# author: William de Paula
# website:
# last edited: 15 de maio de 2017

import simpleaudio as sa
import signal
import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from gi.repository import GObject
import time
from threading import Thread


class Afazer():
    def __init__(self):
        # Valores default
        self.app = 'afazerapp'

        # Valores em minutos
        self.tempo_pomodoro = 25
        self.intervalo = 5
        self.intervalo_longo = 20
        # Quantos pomodoros antes de um intervalo maior
        self.qtd_pomodoros = 5

        # Contador de pomodoros
        self.pomodoros = 0

        # Som de alerta
        self.sominicio = sys.path[0] + '/Inicio.wav'
        self.somintervalo = sys.path[0] + '/Intervalo.wav'
        self.somfim = sys.path[0] + '/Fim.wav'

        # Icone do Programa
        self.iconpath = sys.path[0] + '/afazer.svg'

        self.indicator = AppIndicator3.Indicator.new(
            self.app,
            self.iconpath,
            AppIndicator3.IndicatorCategory.OTHER
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.cria_menu())
        self.indicator.set_label("Afazer", self.app)




    def cria_menu(self):
        menu = Gtk.Menu()

        startPomodoroMenuItem = Gtk.MenuItem('Iniciar Pomodoro')
        startPomodoroMenuItem.connect('activate', self.start_pomodoro)
        menu.append(startPomodoroMenuItem)

        # Separador
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)

        # quit
        item_quit = Gtk.MenuItem("Quit")
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def start_pomodoro(self, source):

        # Inicia Pomodoro
        self.pomodoros += 1
        self.update = Thread(target=self.Pomodoro)
        self.update.setDaemon(True)
        self.update.start()


    def Pomodoro(self):
        # Toca som de alerta
        som = sa.WaveObject.from_wave_file(self.sominicio)
        som.play()

        t = self.tempo_pomodoro
        self.alerta("Afazer", "Pomodoro inciado, concentração e foco!")
        while t > 0:
            # Adicona zero se o tempo for menor que 10m,
            # para uma melhor apresentação
            if t < 10:
                mensagem = str(self.pomodoros) + "º Pomodoro - 0" + str(t)
            else:
                mensagem = str(self.pomodoros) + "º Pomodoro - " + str(t)

            # Aplica alteração no label do menu usando GObject.idle_add()
            GObject.idle_add(
                self.indicator.set_label,
                mensagem,
                self.app,
                priority=GObject.PRIORITY_DEFAULT
            )

            # Espera 60 segundos
            time.sleep(60)
            t -= 1

        self.alerta("Afazer", "Fim do Pomodoro")

        # Inicia intervalo
        self.update = Thread(target=self.Intervalo)
        self.update.setDaemon(True)
        self.update.start()
        return

    def Intervalo(self):
        # Toca som de alerta
        som = sa.WaveObject.from_wave_file(self.somintervalo)
        som.play()
        # Verifica quantos pomodoros já foram
        if self.pomodoros % self.qtd_pomodoros == 0:
            t = self.intervalo_longo
        else:
            t = self.intervalo

        self.alerta(
            "Afazer",
            "Hora do descanço, faça um intervalo de " + str(t) + " minutos"
            )
        while t > 0:
            # Adicona zero se o tempo for menor que 10m,
            # para uma melhor apresentação
            if t < 10:
                mensagem = "Intervalo"
            else:
                mensagem = str(t)

            # Aplica alteração no label do menu usando GObject.idle_add()
            GObject.idle_add(
                self.indicator.set_label,
                mensagem,
                self.app,
                priority=GObject.PRIORITY_DEFAULT
            )

            # Espera 60 segundos
            time.sleep(60)
            t -= 1

        self.alerta("Afazer", "Fim do Intervalo, hora de retornar ao Trabalho")

        # Aplica alteração no label do menu usando GObject.idle_add()
        mensagem = "Afazer"
        GObject.idle_add(
            self.indicator.set_label,
            mensagem,
            self.app,
            priority=GObject.PRIORITY_DEFAULT
        )

        # Toca som de alerta
        som = sa.WaveObject.from_wave_file(self.somfim)
        som.play()
        return


    # Exibe as notificações e alertas
    def alerta(self, titulo, mensagem):

        # Exibe notificação
        Notify.init(self.app)
        Notify.Notification.new(titulo, mensagem, None).show()
        return



    def quit(self, source):
        Gtk.main_quit()


if __name__ == "__main__":

    Afazer()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
