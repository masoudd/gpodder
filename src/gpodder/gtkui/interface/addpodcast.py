# -*- coding: utf-8 -*-
#
# gPodder - A media aggregator and podcast client
# Copyright (c) 2005-2018 The gPodder Team
#
# gPodder is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import Gdk, Gtk

import gpodder
from gpodder import util
from gpodder.gtkui.interface.common import BuilderWidget

_ = gpodder.gettext


class gPodderAddPodcast(BuilderWidget):
    def new(self):
        self.gPodderAddPodcast.set_transient_for(self.parent_widget)
        if not hasattr(self, 'add_podcast_list'):
            self.add_podcast_list = None
        if hasattr(self, 'custom_label'):
            self.label_add.set_text(self.custom_label)
        if hasattr(self, 'custom_title'):
            self.gPodderAddPodcast.set_title(self.custom_title)
        if hasattr(self, 'preset_url'):
            self.entry_url.set_text(self.preset_url)
        self.entry_url.connect('activate', self.on_entry_url_activate)
        self.entry_url.connect('icon-press', self.on_clear_url)
        self.gPodderAddPodcast.show()

        if not hasattr(self, 'preset_url'):
            # Fill the entry if a valid URL is in the clipboard, but
            # only if there's no preset_url available (see bug 1132).
            # First try from CLIPBOARD (everyday copy-paste),
            # then from SELECTION (text selected and pasted via
            # middle mouse button).
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

            def receive_clipboard_text(clipboard, text, second_try):
                # Heuristic: If space is present in clipboard text
                # normalize_feed_url will either fix to valid url or
                # return None if URL cannot be validated
                if text is not None:
                    url = util.normalize_feed_url(text)
                    if url is not None:
                        self.entry_url.set_text(url)
                        self.entry_url.set_position(-1)
                        return

                if not second_try:
                    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
                    clipboard.request_text(receive_clipboard_text, True)
            clipboard.request_text(receive_clipboard_text, False)

    def on_clear_url(self, widget, icon_position, event):
        self.entry_url.set_text('')

    def on_btn_close_clicked(self, widget):
        self.gPodderAddPodcast.destroy()

    def on_btn_paste_clicked(self, widget):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.request_text(self.receive_clipboard_text)

    def receive_clipboard_text(self, clipboard, text, data=None):
        if text is not None:
            self.entry_url.set_text(text.strip())
        else:
            self.show_message(_('Nothing to paste.'), _('Clipboard is empty'))

    def on_entry_url_changed(self, widget):
        self.btn_add.set_sensitive(self.entry_url.get_text().strip() != '')

    def on_entry_url_activate(self, widget):
        self.on_btn_add_clicked(widget)

    def on_btn_add_clicked(self, widget):
        url = self.entry_url.get_text()
        self.on_btn_close_clicked(widget)
        if self.add_podcast_list is not None:
            title = None  # FIXME: Add title GUI element
            self.add_podcast_list([(title, url, None)])
