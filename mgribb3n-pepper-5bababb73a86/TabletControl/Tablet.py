# -*- coding: utf-8 -*-

import time

class Tablet(object):
    def __init__(self, session, web_view_scale_factor=1.34, security="wpa2", ssid="Pepper", password="robotpepper"):
        """
        init
        :param session: qi session
        :param web_view_scale_factor: scale factor of web view  (1.34 is default)
        :param security: web security of router
        :param ssid: ssid of router
        :param password: router password
        """
        self.tablet_service = session.service("ALTabletService")
        if not self.tablet_service.getWifiStatus() in "CONNECTED": # Checks if the tablet is already connected.
            print "Connecting to tablet: Please wait"
            self.tablet_service.setOnTouchWebviewScaleFactor(float(web_view_scale_factor))
            self.tablet_service.configureWifi(security, ssid, password)
            self.tablet_service.connectWifi("Pepper")
            time.sleep(10)
        else:
            time.sleep(1)

        self.set_background_color() # Sets web-view background color to white.

    # Shows an image on the tablet.
    def show_image(self, image_url):
        self.tablet_service.showImage(image_url)

    # Shows an image on the tablet.
    # Loads the image with no cache.
    def show_image_no_cache(self, image_url):
        self.tablet_service.showImageNoCache(image_url)

    # Hides the current image.
    def hide_image(self):
        self.tablet_service.hideImage()

    # Plays a video on the tablet.
    def play_video(self, video_url):
        self.tablet_service.playVideo(video_url)

    # Pauses the current video.
    def pause_video(self):
        self.tablet_service.pauseVideo()

    # Resumes the current video.
    def resume_video(self):
        self.tablet_service.resumeVideo()

    # Stops the current video.
    def stop_video(self):
        self.tablet_service.stopVideo()

    # Shows a web page on the tablet.
    def show_web_view(self, url):
        self.tablet_service.showWebview(url)

    # Hides the current web page.
    def hide_web_view(self):
        self.tablet_service.hideWebview()

    # Cleans the tablet browser.
    def clean_web_view(self):
        self.tablet_service.cleanWebview()

    # Sets the background color.
    # Uses HEX color values.
    # Default color is white.
    def set_background_color(self, color="#FFFFFF"):
        self.tablet_service.setBackgroundColor(color)

    # Resets the tablet.
    def reset_tablet(self):
        self.tablet_service.resetTablet()

    # Shows an input text dialog.
    def show_input_text_dialog(self, title="title", button="ok", cancel="cancel"):
        self.tablet_service.showInputTextDialog(title, button, cancel)

    # Executes a java script.
    def execute_java_script(self, url):
        self.tablet_service.executeJS(url)