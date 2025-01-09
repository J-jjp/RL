import pygame
import threading
import time

# 定义手柄读取线程
class JoystickThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        # 初始化 Pygame 和手柄
        pygame.init()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("No joystick connected.")
            return

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick name: {joystick.get_name()}")

        # 开始读取手柄输入
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    for i in range(joystick.get_numaxes()):
                        axis_value = joystick.get_axis(i)
                        print(f"Axis {i} value: {axis_value}")
                if event.type == pygame.JOYBUTTONDOWN:
                    for i in range(joystick.get_numbuttons()):
                        if joystick.get_button(i):
                            print(f"Button {i} pressed")
                if event.type == pygame.JOYHATMOTION:
                    for i in range(joystick.get_numhats()):
                        hat_value = joystick.get_hat(i)
                        print(f"Hat {i} value: {hat_value}")

            # 控制线程的刷新频率
            time.sleep(0.01)

        # 结束时清理
        pygame.joystick.quit()
        pygame.quit()

    def stop(self):
        self.running = False

# 主线程
if __name__ == "__main__":
    joystick_thread = JoystickThread()
    joystick_thread.start()

    try:
        # 主线程可以进行其他任务
        while True:
            print("Main thread is running...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping joystick thread...")
        joystick_thread.stop()
        joystick_thread.join()
