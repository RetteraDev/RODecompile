#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/minicc.o
import json
import BigWorld
import gamelog
g_event_timer = None
g_notify_cb = None
mini_cc = None

def init(notify_cb):
    global g_notify_cb
    g_notify_cb = notify_cb
    _start()


def reset():
    global g_notify_cb
    g_notify_cb = None
    _stop()


def create_session(session_id = 0):
    json_data = '{\"type\":\"create-session\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def destory_session(session_id = 0):
    json_data = '{\"type\":\"destroy-session\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def login_session(json_info, session_id = 0):
    json_data = '{\"type\":\"login-session\", \"session-id\":%d, \"info\":%s}' % (session_id, json_info)
    controlMini(json_data, 0)
    print 'bgf@login_session', json_data


def logout_session(session_id = 0):
    json_data = '{\"type\":\"logout-session\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def start_capture(session_id = 0):
    json_data = '{\"type\":\"start-capture\", \"session-id\":%d, \"stereo\": 0}' % session_id
    controlMini(json_data, 0)


def stop_capture(session_id = 0):
    json_data = '{\"type\":\"stop-capture\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def set_capture_boost(boost, session_id = 0):
    json_data = '{\"type\":\"set-capture-boost\", \"session-id\":%d, \"boost\": %s}' % (session_id, boost)
    controlMini(json_data, 0)


def mute_capture(mute, session_id = 0):
    json_data = '{\"type\":\"mute-capture\", \"session-id\":%d, \"mute\":%d}' % (session_id, mute)
    controlMini(json_data, 0)


def mute_playback(mute, session_id = 0):
    json_data = '{\"type\":\"mute-playback\", \"session-id\":%d, \"mute\":%d}' % (session_id, mute)
    controlMini(json_data, 0)


def set_playback_vol(percent, session_id = 0):
    json_data = '{\"type\":\"set-playback-vol\", \"session-id\":%d, \"percent\":%d}' % (session_id, percent)
    controlMini(json_data, 0)


def set_playback_volume(volume):
    json_data = '{\"type\":\"set-playback-volume\", \"volume\":%d}' % volume
    controlMini(json_data, 0)


def set_capture_volume(volume):
    json_data = '{\"type\":\"set-capture-volume\", \"volume\":%d}' % volume
    controlMini(json_data, 0)


def ignore_voice(eid, ignore, session_id = 0):
    json_data = '{\"type\":\"ignore-voice\", \"session-id\":%d, \"eid\":%d, \"ignore\":%d}' % (session_id, eid, ignore)
    controlMini(json_data, 0)


def start_record(path, rtype, session_id = 0):
    json_data = '{\"type\":\"record-open\", \"session-id\":%d, \"path\":\"%s\", \"record-type\":%d}' % (session_id, path, rtype)
    controlMini(json_data, 0)


def stop_record(session_id = 0):
    json_data = '{\"type\":\"record-close\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def test_mic(start, session_id = 0):
    json_data = '{\"type\":\"test-mic\", \"session-id\":%d, \"start\":%d}' % (session_id, start)
    controlMini(json_data, 0)


def get_speaking_list(session_id = 0):
    json_data = '{\"type\":\"get-speaking-list\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def get_capture_energy(session_id = 0):
    json_data = '{\"type\":\"get-capture-energy\", \"session-id\":%d}' % session_id
    controlMini(json_data, 0)


def get_capture_device_list():
    json_data = '{\"type\":\"get-capture-device-list\"}'
    controlMini(json_data, 0)


def get_capture_device_volume():
    json_data = '{\"type\":\"get-capture-device-volume\"}'
    controlMini(json_data, 0)


def get_playback_device_list():
    json_data = '{\"type\":\"get-playback-device-list\"}'
    controlMini(json_data, 0)


def get_playback_device_volume():
    json_data = '{\"type\":\"get-playback-device-volume\"}'
    controlMini(json_data, 0)


def set_capture_volume(val):
    json_data = '{\"type\":\"set-capture-volume\", \"volume\":%d}' % val
    controlMini(json_data, 0)


def set_playback_volume(val):
    json_data = '{\"type\":\"set-playback-volume\", \"volume\":%d}' % val
    controlMini(json_data, 0)


def set_capture_device(device_id):
    json_data = '{\"type\":\"set-capture-device\", \"device-id\":%d}' % device_id
    controlMini(json_data, 0)


def set_playback_device(device_id):
    json_data = '{\"type\":\"set-playback-device\", \"device-id\":%d}' % device_id
    controlMini(json_data, 0)


def set_ec_level(level):
    json_data = '{\"type\":\"set-ec-level\", \"level\":%d}' % level
    controlMini(json_data, 0)


def set_ns_level(level):
    json_data = '{\"type\":\"set-ns-level\", \"level\":%d}' % level
    controlMini(json_data, 0)


def reset_engine():
    json_data = '{\"type\":\"reset-engine\"}'
    controlMini(json_data, 0)


def update_position(pos, lookat, session_id = 0):
    json_data = '{\"type\":\"update-position\", \"pos\": {\"x\": %.2f, \"y\": %.2f}, \"at\": {\"x\": %.2f, \"y\": %.2f }, \"session-id\": %d}' % (pos[0],
     pos[2],
     lookat[0],
     lookat[2],
     session_id)
    controlMini(json_data, 0)


def enable_receiver3D(enable = 1, session_id = 0):
    json_data = '{\"type\":\"enable-receiver3D\", \"enable\": %d, \"session-id\": %d}' % (enable, session_id)
    controlMini(json_data, 0)


def set_source3D_radius(radius = 5.0):
    json_data = '{\"type\":\"setting-source3D-radius\", \"radius\": %.2f}' % radius
    controlMini(json_data, 0)


def enable_pitch(enable, origin, target, adjustment = 0):
    json_data = '{\"type\":\"enable-pitch\", \"enable\": %d, \"origin\": %d, \"target\": %d, \"adjustment\": %d}' % (enable,
     origin,
     target,
     adjustment)
    controlMini(json_data, 0)


def controlMini(json_data, param):
    global mini_cc
    if not mini_cc or not hasattr(mini_cc, 'controlMini'):
        return
    mini_cc.controlMini(json_data, param)


def _start():
    global mini_cc
    mini_cc = BigWorld.PyCC()
    if not mini_cc or not hasattr(mini_cc, 'startCCMini'):
        return
    result = mini_cc.startCCMini()
    gamelog.debug('bgf@miniCC _start', result)
    if result != -1:
        _handle_notify()


def _stop():
    global mini_cc
    if not mini_cc or not hasattr(mini_cc, 'closeCCMini'):
        return
    mini_cc.closeCCMini()
    mini_cc = None


def _handle_notify():
    global g_event_timer
    if g_event_timer:
        BigWorld.cancelCallback(g_event_timer)
        g_event_timer = None
    if not mini_cc:
        return
    for i in xrange(10):
        result = mini_cc.getJsonData(0)
        if result is None:
            break
        if result <= 0:
            break
        json_data = json.loads(result)
        if g_notify_cb is not None:
            g_notify_cb(json_data)

    g_event_timer = BigWorld.callback(0.1, _handle_notify)
