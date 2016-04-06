from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, \
    NumericProperty
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

#Jnius android stuff
from jnius import autoclass, PythonJavaClass, java_method, cast
from android.runnable import run_on_ui_thread

#preload java classes
System = autoclass('java.lang.System')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
#KontaktSDK = autoclass('com.kontakt.sdk.common.KontaktSDK')
#ProximityManager = autoclass('com.kontakt.sdk.android.ble.manager.ProximityManager')


class BeaconRoot(BoxLayout):


    def __init__(self, **kwargs):
        super(BeaconRoot, self).__init__(**kwargs)
#        KontaktSDK.initialize("apikeyhere")
 #       self.proximityManagerContract = autoclass('com.kontakt.sdk.android.manager.KontaktProximityManager')
        Clock.schedule_once(self.onStart)

    def onStart(self, dt):
  #      proximityManagerContract.initializeScan(ProximityManager.getScanContext())
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')

        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.arse('http://kivy.org'))

        currentActivity = cast('android.app.Activity', PythonActivity.mAtivity)
        currentActivity.startActivity(intent)


class BeaconApp(App):

    def __init__(self, **kwargs):
        super(BeaconApp, self).__init__(**kwargs)

    def build(self):
        return BeaconRoot()
