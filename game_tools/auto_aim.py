import pymem
import pymem.process
import keyboard
import math
import time


# =========================================================
# 3. الدوال الحسابية (Math Helpers)
# =========================================================
def calculate_angle(player_pos, enemy_pos):
    """
    حساب زوايا الرؤية (Pitch & Yaw) المطلوبة للتوجيه من موقعك إلى رأس العدو
    """
    dx = enemy_pos[0] - player_pos[0]
    dy = enemy_pos[1] - player_pos[1]
    dz = enemy_pos[2] - player_pos[2]

    # حساب المسافة الأفقية
    horizontal_dist = math.sqrt(dx * dx + dy * dy)

    # حساب زاوية Yaw (الدوران الأفقي)
    yaw = math.degrees(math.atan2(dy, dx))

    # حساب زاوية Pitch (الارتفاع العمودي)
    pitch = math.degrees(math.atan2(dz, horizontal_dist))

    return pitch, yaw

def get_angle_distance(current_pitch, current_yaw, target_pitch, target_yaw):
    """
    حساب الفرق الزاوي (FOV Distance) بين نقطة التصويب الحالية ورأس العدو
    """
    diff_pitch = abs(target_pitch - current_pitch)
    diff_yaw = abs(target_yaw - current_yaw)
    
    # التعامل مع تعدي الزوايا 360 درجة
    if diff_yaw > 180:
        diff_yaw = 360 - diff_yaw

    return math.sqrt(diff_pitch**2 + diff_yaw**2)

