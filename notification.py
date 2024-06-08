'''
Module of Android API for plyer.notification.

.. versionadded:: 1.0.0

.. versionchanged:: 1.4.0
    Fixed notifications not displaying due to missing NotificationChannel
    required by Android Oreo 8.0+ (API 26+).

.. versionchanged:: 1.4.0
    Added simple toaster notification.

.. versionchanged:: 1.4.0
    Fixed notifications not displaying big icons properly.
    Added option for custom big icon via `icon`.

.. versionchanged:: 1.5.0
    Fixed notifications. Changed getting activity depending on api_version >= 31
    Functon _set_icons has been refactored.
    Added text style property for large message.
'''

from typing import Optional

from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

from jnius import autoclass, cast

from android import python_act, api_version
from android.runnable import run_on_ui_thread

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationManager = autoclass('android.app.NotificationManager')

NotificationBuilder = autoclass('android.app.Notification$Builder')
BigTextStyle = autoclass('android.app.Notification$BigTextStyle')

Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
Toast = autoclass('android.widget.Toast')
BitmapFactory = autoclass('android.graphics.BitmapFactory')


class AndroidNotification(Notification):
    """ Implementation of Android notification API.

        .. versionadded:: 1.0.0
    """
    def __init__(self):
        self._ns = None
        self._channel_id = activity.getPackageName()

    def _get_notification_service(self):
        if not self._ns:
            self._ns = cast(NotificationManager, activity.getSystemService(
                Context.NOTIFICATION_SERVICE
            ))
        return self._ns

    def _build_notification_channel(self, name: str) -> Optional[autoclass]:
        """ Create a NotificationChannel using channel id of the application
            package name (com.xyz, org.xyz, ...) and channel name same as the
            provided notification title if the API is high enough, otherwise
            do nothing.

            .. versionadded:: 1.4.0

        Args:
            name (str): notification title

        Returns:
            Optional[autoclass]: autoclass
        """
        if SDK_INT < 26:
            return None

        channel = autoclass('android.app.NotificationChannel')

        self.app_channel = channel(
            self._channel_id, name, NotificationManager.IMPORTANCE_DEFAULT
        )
        self._get_notification_service().createNotificationChannel(
            self.app_channel
        )
        return self.app_channel

    @run_on_ui_thread
    def _toast(self, message: str) -> None:
        """ Display a popup-like small notification at the bottom of the screen.

            .. versionadded:: 1.4.0

        Args:
            message (str): notify msg
        """
        Toast.makeText(
            activity,
            cast('java.lang.CharSequence', AndroidString(message)),
            Toast.LENGTH_LONG
        ).show()

    @staticmethod
    def _set_icons(notification: autoclass, notif_icon: str=None) -> None:
        """ Set the small application icon displayed at the top panel together with
            WiFi, battery percentage and time and the big optional icon (preferably
            PNG format with transparent parts) displayed directly in the
            notification body.

            .. versionadded:: 1.5.0

        Args:
            notification (autoclass): autoclass
            notif_icon (str): name of icon in drawable folder
        """
        if notif_icon is not None:
            icon_name, _ = notif_icon.split('.')
            small_icon = getattr(Drawable, icon_name)
            notification.setSmallIcon(small_icon)

            bitmap_icon = BitmapFactory.decodeFile(notif_icon)
        else:
            # icon == None, use the app icon as a small notification icon
            app_icon = Drawable.icon
            notification.setSmallIcon(app_icon)

            bitmap_icon = BitmapFactory.decodeResource(
                python_act.getResources(), app_icon
            )

        notification.setLargeIcon(bitmap_icon)

    def _build_notification(self, title: str) -> None:
        """ Build notification object.

            .. versionadded:: 1.4.0

        Args:
            title (str): title of notification

        Returns:
            autoclass
        """
        if SDK_INT < 26:
            notif = NotificationBuilder(activity)
        else:
            self._build_notification_channel(title)
            notif = NotificationBuilder(activity, self._channel_id)
        return notif

    @staticmethod
    def _set_open_behavior(notification: autoclass) -> None:
        """ Open the source application when user opens the notification.

            .. versionadded:: 1.5.0

        Args:
            notification (autoclass): autoclass
        """

        # create Intent that navigates back to the application
        app_context = activity.getApplication().getApplicationContext()
        notification_intent = Intent(app_context, python_act)

        # set flags to run application Activity
        notification_intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        notification_intent.setAction(Intent.ACTION_MAIN)
        notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)

        # get application Activity
        if api_version >= 31:
            pending_intent = PendingIntent.getActivity(
                app_context, 0, notification_intent, PendingIntent.FLAG_MUTABLE
            )
        else:
            pending_intent = PendingIntent.getActivity(
                app_context, 0, notification_intent, PendingIntent.FLAG_IMMUTABLE  # 0
            )

        notification.setContentIntent(pending_intent)
        notification.setAutoCancel(True)

    def _send_notification(self, notification: autoclass) -> None:
        """ Send notification with care about the sdk dependency.

        Args:
            notification (autoclass): autoclass
        """
        if SDK_INT >= 16:
            notification = notification.build()
        else:
            notification = notification.getNotification()

        self._get_notification_service().notify(0, notification)

    def _notify(self, **kwargs):
        """ Notify core function.

            .. versionadded:: 1.4.0
        """
        notif = None
        message = kwargs.get('message').encode('utf-8')
        ticker = kwargs.get('ticker').encode('utf-8')
        title = AndroidString(
            kwargs.get('title', '').encode('utf-8')
        )
        notif_icon = kwargs.get('app_icon')

        # decide whether toast only or proper notification
        if kwargs.get('toast'):
            self._toast(message)
            return
        else:
            notif = self._build_notification(title)

        # set basic properties for notification
        notif.setContentTitle(title)
        notif.setContentText(AndroidString(message))
        notif.setTicker(AndroidString(ticker))

        # set big text style property for large message
        notif.setStyle(BigTextStyle().bigText(message))

        # set additional flags for notification
        self._set_icons(notif, notif_icon)
        self._set_open_behavior(notif)

        # notif launch
        self._send_notification(notif)


def instance():
    """ Instance for facade proxy.
    """
    return AndroidNotification()
