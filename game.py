import pymem
import pymem.process
import keyboard
import math
import time
from game_tools.auto_aim import calculate_angle,get_angle_distance

# =========================================================
# 1. إعدادات العناوين (Addresses & Offsets)
# قومي بإدخال العناوين التي تجدها بنفسك هنا
# =========================================================
PROCESS_NAME = "game_name.exe" # استبدل باسم العملية الخاصة باللعبة

# عناوين كاميرا زاوية الرؤية الخاصة بك (Local Player / Camera Pitch & Yaw)
ADDR_PLAYER_PITCH = 0x00000000 # عنوان زاوية النظر العمودية (Pitch: X/Up-Down)
ADDR_PLAYER_YAW = 0x00000000 # عنوان زاوية النظر الأفقية (Yaw: Y/Left-Right)

# عناوين إحداثيات رأس العدو في العالم (Enemy Head X, Y, Z)
ADDR_ENEMY_HEAD_X = 0x00000000 # إحداثيات العدو X
ADDR_ENEMY_HEAD_Y = 0x00000000 # إحداثيات العدو Y
ADDR_ENEMY_HEAD_Z = 0x00000000 # إحداثيات العدو Z

# عناوين إحداثيات اللاعب الخاص بك (Local Player X, Y, Z)
ADDR_PLAYER_X = 0x00000000 # إحداثيات موقعك X
ADDR_PLAYER_Y = 0x00000000 # إحداثيات موقعك Y
ADDR_PLAYER_Z = 0x00000000 # إحداثيات موقعك Z

# =========================================================
# 2. إعدادات الأيم والمسافة (Aim Assist Settings)
# =========================================================
SHOOT_KEY = "ctrl" # زر إطلاق النار (يمكنك تغييره إلى 'shift' أو أي زر آخر)
MAX_FOV_THRESHOLD = 5.0 # مسافة الأيم المسموح بها (درجات) - كلما صغرت الرقم كلما اشترط قرب الأيم أكثر من العدو

# =========================================================
# 4. الحلقة الرئيسية (Main Loop)
# =========================================================
def main():
    try:
        pm = pymem.Pymem(PROCESS_NAME)
        print(f"[+] تم الاتصال باللعبة بنجاح: {PROCESS_NAME}")
    except Exception as e:
        print(f"[-] تعذر الاتصال باللعبة: {e}")
        return

    print(f"[+] اضغط واستمر بالضغط على زر [{SHOOT_KEY}] للتفعيل عند الاقتراب من العدو...")

    while True:
        try:
            # الشرط الأول: التحقق من إيقاف أو تفعيل السكربت بزر إطلاق النار
            if keyboard.is_pressed(SHOOT_KEY):
                
                # قراءة موقعك الحالي
                p_x = pm.read_float(ADDR_PLAYER_X)
                p_y = pm.read_float(ADDR_PLAYER_Y)
                p_z = pm.read_float(ADDR_PLAYER_Z)

                # قراءة موقع رأس العدو
                e_x = pm.read_float(ADDR_ENEMY_HEAD_X)
                e_y = pm.read_float(ADDR_ENEMY_HEAD_Y)
                e_z = pm.read_float(ADDR_ENEMY_HEAD_Z)

                # قراءة زوايا الأيم الحالية الخاصة بك
                curr_pitch = pm.read_float(ADDR_PLAYER_PITCH)
                curr_yaw = pm.read_float(ADDR_PLAYER_YAW)

                # حساب الزاوية المستهدفة للوصول لرأس العدو
                target_pitch, target_yaw = calculate_angle((p_x, p_y, p_z), (e_x, e_y, e_z))

                # حساب المسافة الزاوية بين الأيم ورأس العدو
                fov_dist = get_angle_distance(curr_pitch, curr_yaw, target_pitch, target_yaw)

# الشرط الثاني: المساعدة فقط إذا كان الأيم قريباً جداً من رأس العدو
                if fov_dist <= MAX_FOV_THRESHOLD:
                    # كتابة الزوايا الجديدة في ذاكرة اللعبة لقفل الأيم على الرأس
                    pm.write_float(ADDR_PLAYER_PITCH, target_pitch)
                    pm.write_float(ADDR_PLAYER_YAW, target_yaw)

            # سرعة التحديث لتجنب الضغط على المعالج
            time.sleep(0.005)

        except Exception as e:
            # في حال حدوث خطأ في قراءة الذاكرة أثناء إغلاق اللعبة أو إعادة الترسيت
            time.sleep(0.1)

if name == "main":
    main()
    
