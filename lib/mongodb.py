from .component import Component
from .optional import Optional
from .persistent import Persistent
from .optional import Optional
from .quantifiable import Quantifiable
from .authenticable import Authenticable
from .constants import mongo as constants

import getpass

class MongoDB(Component):

    def __init__(self):
        super().__init__()
        self._visible_name = constants['name']
        self.__super_username = "mongodb"
        self.__super_password = "mongodb"
        self.__persistence_time = 168
        self.__use_persistent_volume = False
        self.__volume_size = 10
        self.__authenticable = Authenticable()  
        self.__persistent = Persistent()     
        self.__optional = Optional()
        self.__quantifiable = Quantifiable()

    def ask_super_username(self):
        self.__super_username = self.__authenticable.ask_username(constants['super_user'].format( self.__super_username ), self.__super_username)
        return self

    def and_super_password(self):
        self.__super_password = self.__authenticable.ask_password(constants['super_password'].format( self.__super_password ), self.__super_password)
        return self

    def and_persistence_time(self):
        self.__persistence_time = self.__quantifiable.ask_quantity(constants['persistence_time'].format( self.__persistence_time), default=self.__persistence_time)
        return self

    def and_if_use_persistent_volume(self):
        self.__use_persistent_volume = self.__optional.ask_use(constants['use_persistent_volume'])
        return self

    def and_volume_size(self):
        if self.__use_persistent_volume:
            self.__volume_size = self.__quantifiable.ask_quantity(constants['volume_size'].format( self.__volume_size))
        return self

    @property
    def vars(self):
        self._vars['dojot_mongodb_super_user'] = self.__super_username
        self._vars['dojot_mongodb_super_passwd'] = self.__super_password
        self._vars['dojot_mongodb_persistent_volumes'] = self.__use_persistent_volume
        self._vars['dojot_mongodb_volume_size'] = self.__volume_size
        self._vars['dojot_persister_persistence_time'] = self.__persistence_time
        return self._vars