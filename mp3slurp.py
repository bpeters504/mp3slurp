#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
import gi, re, os, yaml, sys, eyed3, threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
from os.path import expanduser


## Simple GTK 3 wrapper for youtube-dl to create MP3 audio files
## from a list of youtube URLs.
## Also allows ID3 tagging for Title and Artist.

## Global variables
download_dir = ''
cfg = {}




class EntryWindow(Gtk.Window):

    def addrow(self, add_button, myGrid):
        
        ## url label
        self.url_label = Gtk.Label()
        self.url_label.set_text("URL:")
        self.url_label.set_size_request(10, 30)

        ## url Entry
        self.url_entry = Gtk.Entry()
        self.url_entry.set_width_chars(50)
        self.url_entry.set_has_frame(True)
        #self.url_entry.set_text('https://www.youtube.com/watch?v=8R6StQfLNbw')

        ## title label
        self.title_label = Gtk.Label()
        self.title_label.set_text("Title:")
        self.title_label.set_size_request(10, 30)

        ## title Entry
        self.title_entry = Gtk.Entry()
        self.title_entry.set_width_chars(20)
        self.title_entry.set_has_frame(True)
        #self.title_entry.set_text('Have a Cigar (Pink Floyd)')

        ## artist label
        self.artist_label = Gtk.Label()
        self.artist_label.set_text("Artist:")
        self.artist_label.set_size_request(10, 30)
        
        ## artist Entry
        self.artist_entry = Gtk.Entry()
        self.artist_entry.set_width_chars(20)
        self.artist_entry.set_has_frame(True)
        #self.artist_entry.set_text('The Main Squeeze')

        ## Spinner
        self.spinner = Gtk.Spinner()
        self.result_label = Gtk.Label()

        ## Entry Grid
        myGrid.set_column_spacing(20)
        rowIndex = len(myGrid)
        myGrid.attach(self.url_label, 0, rowIndex, 1, 1)
        myGrid.attach(self.url_entry, 1, rowIndex, 1, 1)
        myGrid.attach(self.artist_label, 2, rowIndex, 1, 1)
        myGrid.attach(self.artist_entry, 3, rowIndex, 1, 1)
        myGrid.attach(self.title_label, 4, rowIndex, 1, 1)
        myGrid.attach(self.title_entry, 5, rowIndex, 1, 1)
        myGrid.attach(self.spinner, 6, rowIndex, 1, 1)
        myGrid.attach(self.result_label, 7, rowIndex, 1, 1)
        
        myGrid.show_all()

    def __init__(self):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        Gtk.Window.__init__(self, title="YouTube Music Downloader")
        self.set_default_size(1000,100)
        self.set_border_width(10)
        self.timeout_id = None

        ## vbox - outer box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_valign(Gtk.Align.START)

        ## hbox1 - message label and buttons
        hbox1 = Gtk.Box(spacing=6)

        ## message label
        self.label = Gtk.Label()
        self.label.set_text("")
        self.label.set_width_chars(32)
        #hbox1.pack_start(self.label, False, False, 0)
        
        ## data entry grid
        entryGrid = Gtk.Grid()
        entryGrid.set_column_spacing(20)

        vbox.pack_start(hbox1, False, False, 0)
        vbox.pack_end(entryGrid, False, False, 0)
        self.add(vbox)

        ## hbox3 - buttons
        hbox3 = Gtk.Box(spacing=6)
        vbox.pack_end(hbox3, False, False, 0)

        hbox3.pack_start(self.label, False, False, 0)
        ## Download Button
        submit_button = Gtk.Button.new_with_label("Download")
        submit_button.connect("clicked", self.submit_button_clicked, entryGrid)
        hbox3.pack_end(submit_button, False, False, 0)
        
        ## Add Button
        add_button = Gtk.Button.new_with_label("Add Another")
        add_button.connect("clicked", self.addrow, entryGrid)
        hbox3.pack_end(add_button, False, False, 0)

        ## add the first row of entry fields by forcing a click event
        add_button.clicked()

    def submit_button_clicked(self, submit_button, entryGrid):
        child_range = range(0, len(entryGrid), 8)
        self.label.set_text("Writing files to: "+download_dir)
        for top in child_range:
            url = entryGrid.get_child_at(1,top).get_text()
            artist = entryGrid.get_child_at(3,top).get_text()
            title = entryGrid.get_child_at(5,top).get_text()
            spinner = entryGrid.get_child_at(6,top)
            result_label = entryGrid.get_child_at(7,top)
            dl_thread = threading.Thread(target=self.download, args=(url, artist, title, spinner, result_label))
            dl_thread.start()

    def download(self, url, artist, title, spinner, result_label):
        ## if there is no URL, do nothing.
        if url is '':
            result_label.set_text('Empty URL')
            return
        spinner.start()
        result_label.set_text('Downloading')
        ydl_opts = cfg['youtube_dl']

        ## If title or artist is not specified, outtmpl uses id for filename.
        if title is '' or artist is '':
            ydl_opts['outtmpl'] = download_dir + "/%(id)s" + ".%(ext)s"
        else:
            ydl_opts['outtmpl'] = download_dir +"/" + title.replace(" ", "_") + '-' + artist.replace(" ", "_") + '.%(ext)s'
                    
        ## Download the file
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl_info = ydl.extract_info(url, download=True)
                ## If title or artist is not specified, filename is id
                if title is '' or artist is '':
                    file_dest = download_dir + "/" + ydl_info['id'] + ".mp3"
                else:
                    file_dest = download_dir +"/" + title.replace(" ", "_") + '-' + artist.replace(" ", "_") + '.mp3'
            except:
                spinner.stop()
                result_label.set_text('ERROR!')
                return
        try:
            ## Write the ID3 tags
            mp3file = eyed3.load(file_dest)
            if title is not '':
                mp3file.tag.title = title
            if artist is not '':
                mp3file.tag.artist = artist
            mp3file.tag.save()
        except:
            spinner.stop()
            result_label.set_text('ERROR!')
            return
        spinner.stop()
        result_label.set_text('Done')
        
    
def load_config():
        global download_dir
        global cfg
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        with open(dname + "/config.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        
        if '~' in cfg['mp3slurp']['download_dir']:
            cfg['mp3slurp']['download_dir'] = expanduser(cfg['mp3slurp']['download_dir'])
        if cfg['mp3slurp']['download_dir'] and os.path.isdir(cfg['mp3slurp']['download_dir']):
            download_dir = cfg['mp3slurp']['download_dir']
        elif os.path.isdir(os.environ['HOME']+'/Downloads'):
            download_dir = os.environ['HOME']+'/Downloads'
        elif os.path.isdir(os.environ['HOME']):
            download_dir = os.environ['HOME']
        else:
            sys.exit('ERROR: Cannot find directory to write to. You should configure this in config.yml')

        ## These configs were in the config file but since the user can't
        ## change anything without it breaking the app. I've moved them here
        cfg['youtube_dl'] = {}
        cfg['youtube_dl']['format'] = 'bestaudio/best'
        cfg['youtube_dl']['noplaylist'] = True
        cfg['youtube_dl']['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                                                        'preferredcodec': 'mp3',
                                                        'preferredquality': '192',},
                                                {'key': 'FFmpegMetadata'}]


def main():
    def gtk_style():
        cssProvider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    load_config()
    gtk_style()
    win = EntryWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.set_name("EntryWindow")
    win.show_all()
    Gtk.main()


main()