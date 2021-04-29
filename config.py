#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai


__license__   = 'GPL v3'
__copyright__ = '2011, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

from qt.core import QWidget, QHBoxLayout, QLabel, QLineEdit

from calibre.utils.config import JSONConfig

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/ao3_metadata_plugin_config')

# Set defaults
prefs.defaults['fandoms'] = [None]
prefs.defaults['relationships'] = [None]

class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QHBoxLayout()
        self.setLayout(self.l)

        # self.label = QLabel('Hello world &message:')
        # self.l.addWidget(self.label)

        # self.msg = QLineEdit(self)
        # self.msg.setText(prefs['hello_world_msg'])
        # self.l.addWidget(self.msg)
        # self.label.setBuddy(self.msg)

        self.tag_set_l = QVBoxLayout()
        self.l.addWidget(self.tag_set_l)

        self.tag_list_l = QVBoxLayout()
        self.l.addWidget(self.tag_list_l)

        self.fandom_list_button = QPushButton('Fandoms')
        self.fandom_list_button.clicked.connect(self.show_fandoms)
        self.tag_set_l.addWidget(self.fandom_list_button)

        self.ship_list_button = QPushButton('Relationships')
        self.ship_list_button.clicked.connect(self.show_ships)
        self.tag_set_l.addWidget(self.ship_list_button)

        self.currentTagSet = 'Fandoms'
        self.localTags = {'Fandoms': prefs['Fandoms'],
                        'Relationships': prefs['Relationships']}

        self.new_tag_entry = QLineEdit(self)
        self.new_tag_entry.setText('')
        self.tag_list_l.addWidget(self.new_tag_entry)
        
        self.add_tag_button = QPushButton('Add Tag to Current List')
        self.add_tag_button.clicked.connect(self.add_tag)
        self.tag_list_l.addWidget(self.add_tag_button)

        self.delete_tag_button = QPushButton('Delete Selected Tag')
        self.delete_tag_button.clicked.connect(self.delete_tag)
        self.tag_list_l.addWidget(self.delete_tag_button)

        self.tag_list = QListWidget()
        self.tag_list.itemClicked.connect(self.tag_clicked)
        self.tag_list_l.addWidget(self.tag_list)
        self.show_fandoms()

        self.save_button = QPushButton('Save Current List')
        self.save_button.clicked.connect(self.save_settings)
        self.l.addWidget(self.save_button)

        self.save_status = QLabel('Changes not saved')
        self.l.addWidget(self.save_status)

    def tag_clicked(self, item):
        self.tagToDelete = item.text()

    def save_settings(self):
        prefs[self.currentTagSet] = self.localTags[self.currentTagSet]
        self.save_status.setText('Tags saved!')
    
    def show_fandoms(self):
        self.tag_list.clear()
        self.currentTagSet = 'Fandoms'
        self.tag_list.addItems(list(self.localTags['Fandoms'].values()))

    def show_ships(self):
        self.tag_list.clear()
        self.currentTagSet = 'Relationships'
        self.tag_list.addItems(list(self.localTags['Relationships'].values()))

    def add_tag(self):
        new_tag = str(self.new_tag_entry.text())
        self.localTags[self.currentTagSet].append(new_tag)
        self.new_tag_entry.clear()
        self.save_status.setText('Changes not saved')
        if self.currentTagSet == 'Fandoms':
            self.show_fandoms()
        else:
            self.show_ships()

    def delete_tag(self):
        try:
            tagIndex = self.localTags[self.currentTagSet].find(tagToDelete)
            tag = self.localTags[self.currentTagSet].pop()
            if self.currentTagSet == 'Fandoms':
                self.show_fandoms()
            else:
                self.show_ships()
        except:
            self.save_status('Error: tag to delete does not exist')
