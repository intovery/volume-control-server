from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    return volume.GetMasterVolumeLevelScalar() * 100

def volume_up() -> int:
    current_volume = get_current_volume()
    new_volume = min(100, current_volume + 5) / 100
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    return (int)(new_volume * 100)

def volume_down() -> int:
    current_volume = get_current_volume()
    new_volume = max(0, current_volume - 5) / 100
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    return (int)(new_volume * 100)

def set_volume(target_volume) -> bool:
    if 0 <= target_volume <= 100:
        volume.SetMasterVolumeLevelScalar(target_volume / 100, None)
        return True
    else:
        return False
    
def mute() -> bool:
    current_mute = volume.GetMute()
    new_mute = not current_mute
    volume.SetMute(new_mute, None)
    return new_mute

def get_volume_status():
    current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
    is_muted = volume.GetMute()
    return current_volume, is_muted