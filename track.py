#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import util
from textwrap import wrap

JUSTIFICATION = 0

def justify(lines, width, justification=1):
    if justification == 1:
        return lines
    elif justification == 0:
        return [line.center(width) for line in lines]
    else:
        return [line.rjust(width) for line in lines]


class Track:
    def __init__(self,
                 artist=None,
                 title=None,
                 justify=1,
                 width=0,
                 height=0,
                 hard_format=False):

        self.title = title
        self.artist = artist
        self.justification = justify
        self.hard_format = hard_format
        self.width = width
        self.height = height
        self.length = 0
        self.lyrics = None
        self.album = None
        self.trackid = None
        self.art_url = None

    def __str__(self):
        return self.artist + ' - ' + self.title

    @property
    def track_name(self):
        return self.artist + ' - ' + self.title

    def track_info(self, width):
        trackinfo = justify([self.title, self.artist, self.album], width, self.justification)
        trackinfo = [t + ' ' * (width - len(t)) for t in trackinfo]

        return trackinfo

    def update(self, artist, title, album, trackid, art_url):
        self.artist = artist
        self.title = title
        self.album = album
        self.trackid = trackid
        self.art_url = art_url
        self.get_lyrics()

    def get_lyrics(self):
        self.lyrics = util.get_lyrics(self.track_name)

        if not self.hard_format:
            self.width = len(max(self.lyrics, key=len))

        self.length = len(self.lyrics)

    def justify(self):
        return justify(self.lyrics, self.width, self.justification)

    def format_lyrics(self):
        # center lyrics vertically
        if self.length < self.height and self.hard_format:
            space = (self.height - self.length) // 2
            padding = [''] * (space - 2)
            self.lyrics = padding + self.lyrics + padding

    def wrapped(self, width):
        raw_lyrics = self.lyrics

        lines = []
        for line in self.lyrics:
            if len(line) > width:
                line = wrap(line, width=width)
            if isinstance(line, list):
                lines += line
            else:
                lines.append(line)

        self.width = len(max(lines, key=len))
        self.length = len(lines)

        self.lyrics = lines
        wrapped = self.get_text()
        self.lyrics = raw_lyrics

        return wrapped


    def get_text(self):
        self.format_lyrics()
        lyrics = self.justify()

        self.width = len(max(self.lyrics, key=len))
        self.length = len(self.lyrics)

        return '\n'.join(line for line in lyrics)


if __name__ == '__main__':

    if len(sys.argv) >= 5:
        artist = sys.argv[1].strip()
        title = sys.argv[2].strip()
        width = int(sys.argv[-2])
        height = int(sys.argv[-1])

        track = Track(artist, title, JUSTIFICATION, width, height, True)
        track.get_lyrics()

        topline = [track.track_name, round(width * 0.8) * '-']
        topline = '\n'.join(justify(topline, width, JUSTIFICATION))
        print(topline, '\n' + track.get_text())

    else:
        print('No Track info provided, Exiting...')
        exit
