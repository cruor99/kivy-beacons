from kivy.app import App
from kivy.uix.button import Button

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
BeaconManager = autoclass("org.altbeacon.beacon.BeaconManager")
MonitorNotifier = autoclass("org.altbeacon.beacon.MonitorNotifier")
BeaconParser = autoclass("org.altbeacon.beacon.BeaconParser")
Region = autoclass("org.altbeacon.beacon.Region")


class BeaconActivity(PythonJavaClass):
    __javainterfaces__ = ['org/altbeacon/beacon/BeaconConsumer']
    __javacontext__ = "app"

    def __init__(self):
        self.beaconManager = BeaconManager.getInstanceForApplication(self)
        self.beaconManager.getBeaconParsers().add(BeaconParser().setBeaconLayout("m:0-3=4c000215,i:4-19,i:20-21,i:22-23,p:24-24"))
        self.beaconManager.bind(self)
        self.onBeaconServiceConnect()
        try:
            self.beaconManager.startMonitoringBeaconsInRegion(Region("uniqueIdHere"))
        except:
            print "Something failed"


    @java_method("()V;")
    def onBeaconServiceConnect(self):
        self.beaconManager.setMonitorNotifier(PyMonitorNotifier())



class PyMonitorNotifier(PythonJavaClass):
    __javainterfaces__ = ["org/altbeacon/beacon/MonitorNotifier"]
    __javacontext__ = "app"

    @java_method("(Lorg/altbeacon/beacon/Region)V;")
    def didEnterRegion(self, region):
        print "Found me a beacon or two"


class BeaconRoot(BoxLayout):


    def __init__(self, **kwargs):
        super(BeaconRoot, self).__init__(**kwargs)
        self.beaconactivity = BeaconActivity()
        Clock.schedule_once(self.onStart)

    def onStart(self, dt):
  #      proximityManagerContract.initializeScan(ProximityManager.getScanContext())
        self.add_widget(Button(text="placeholder"))


    def gotoKivy(self, dt):
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')

        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse('http://kivy.org'))

        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)


class BeaconApp(App):

    def __init__(self, **kwargs):
        super(BeaconApp, self).__init__(**kwargs)

    def build(self):
        return BeaconRoot()


if __name__ == "__main__":
    BeaconApp().run()
