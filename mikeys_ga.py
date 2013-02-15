#INPUT BELOW INTO YOUR SETTINGS.XML
#<setting id="ga_time" type="text" label="GA Called" default="0" visible="false"/>
#<setting id="visitor_ga" type="text" label="GA visitor" default="" visible="false"/>

import time
import threading
from functools import wraps

ADDON = xbmcaddon.Addon(id='plugin.YOUR PLUGIN')
PATH = "PLUGIN NAME"  
VERSION = "PLUGIN VERSION" 
UATRACK="UA-xxxxxxxxx-1" #YOUR UA-ANALYTICS NUMBER
VISITOR = ADDON.getSetting('visitor_ga')

def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = time.time()
    prev  = int(ADDON.getSetting('ga_time'))
    delta = now - prev

    if not delta > threshold:
        return

    ADDON.setSetting('ga_time', now)
    APP_LAUNCH()

def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1

            gif_location = "http://www.google-analytics.com/__utm.gif?"
            UTMWV = "utmwv=%s" %VERSION
            UTMN = "&utmn=%s" %str(randint(0, 0x7fffffff))
            UTMCC = "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            if group is not None:
                    utm_track = gif_location + UTMWV + UTMN + \
                            "&utmt=event" + \
                            "&utme="+ quote("5(channel*click*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + UTMCC
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name is not None:
                    utm_url = gif_location + UTMWV + UTMN + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + UTMCC
            else:
                if group is not None:
                       utm_url = gif_location + UTMWV + UTMN + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + UTMCC
                else:
                       utm_url = gif_location + UTMWV + UTMN + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + UTMCC
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        print '==========================   '+PATH+' '+VERSION+'   =========================='
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            import platform
            VISITOR = ADDON.getSetting('visitor_ga')
            try: 
                PLATFORM=platform.system()+' '+platform.release()
            except: 
                PLATFORM=platform.system()
            gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(app*launch*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
checkGA()

def track(group, name):
    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            t = threading.Thread(target = GA, args=(group, name))
            t.start()
            return func(*args, **kwargs)
        return decorator
    return factory