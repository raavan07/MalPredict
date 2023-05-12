from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
from androguard.core.bytecodes.apk import APK
import os
import numpy as np
from keras.models import load_model


model = load_model('My_saved_Model.h5')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
perms = ['android.permission.ACCESS_CACHE_FILESYSTEM',
       'android.permission.ACCESS_COARSE_LOCATION',
       'android.permission.ACCESS_FINE_LOCATION',
       'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS',
       'android.permission.ACCESS_MOCK_LOCATION',
       'android.permission.ACCESS_NETWORK_STATE',
       'android.permission.ACCESS_WIFI_STATE',
       'android.permission.ACCESS_WIMAX_STATE',
       'android.permission.AUTHENTICATE_ACCOUNTS',
       'android.permission.BATTERY_STATS', 'android.permission.BLUETOOTH',
       'android.permission.BROADCAST_PACKAGE_REMOVED',
       'android.permission.BROADCAST_STICKY', 'android.permission.CALL_PHONE',
       'android.permission.CALL_PRIVILEGED', 'android.permission.CAMERA',
       'android.permission.CHANGE_COMPONENT_ENABLED_STATE',
       'android.permission.CHANGE_CONFIGURATION',
       'android.permission.CHANGE_NETWORK_STATE',
       'android.permission.CHANGE_WIFI_MULTICAST_STATE',
       'android.permission.CHANGE_WIFI_STATE',
       'android.permission.CLEAR_APP_CACHE',
       'android.permission.DELETE_PACKAGES', 'android.permission.DEVICE_POWER',
       'android.permission.DISABLE_KEYGUARD', 'android.permission.DUMP',
       'android.permission.EXPAND_STATUS_BAR',
       'android.permission.GET_ACCOUNTS',
       'android.permission.GET_PACKAGE_SIZE', 'android.permission.GET_TASKS',
       'android.permission.INJECT_EVENTS',
       'android.permission.INSTALL_PACKAGES', 'android.permission.INTERNET',
       'android.permission.KILL_BACKGROUND_PROCESSES',
       'android.permission.MANAGE_ACCOUNTS',
       'android.permission.MODIFY_AUDIO_SETTINGS',
       'android.permission.MOUNT_UNMOUNT_FILESYSTEMS',
       'android.permission.NFC', 'android.permission.PROCESS_OUTGOING_CALLS',
       'android.permission.READ_CALENDAR', 'android.permission.READ_CALL_LOG',
       'android.permission.READ_LOGS', 'android.permission.READ_PHONE_STATE',
       'android.permission.READ_SMS',
       'android.permission.RECEIVE_BOOT_COMPLETED',
       'android.permission.RECORD_AUDIO', 'android.permission.SET_ORIENTATION',
       'android.permission.SET_PREFERRED_APPLICATIONS',
       'android.permission.SET_WALLPAPER',
       'android.permission.SYSTEM_ALERT_WINDOW', 'android.permission.VIBRATE',
       'android.permission.WAKE_LOCK',
       'android.permission.WRITE_EXTERNAL_STORAGE',
       'android.permission.WRITE_SETTINGS',
       'com.android.alarm.permission.SET_ALARM',
       'com.android.browser.permission.READ_HISTORY_BOOKMARKS',
       'com.android.launcher.permission.INSTALL_SHORTCUT',
       'com.android.launcher.permission.UNINSTALL_SHORTCUT']



def predict(apk):
    result = []
    a = APK(apk)
    perm = a.get_permissions()
    print(perm)
    for d in perms:
        if d in perm:
            result.append(1)
        else:
            result.append(0)
    return result




app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(path)
        file.save(path)
        if str(path).endswith('.apk'):
            inputarray = predict(path)
            os.remove(path)
            result = np.array(inputarray)
            result = result.reshape((1,-1))
            predictedvalue = model.predict(result)
            malicious = False
            if predictedvalue > 0.5:
                malicious = True
            res = 'Safe'
            if malicious:
                res = 'Malicious'
            return render_template('index.html', val = res)
        else:
            os.remove(path)
            return "Not an APK"


if __name__ == '__main__':
    app.run(debug=True)
