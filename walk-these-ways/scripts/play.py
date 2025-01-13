import isaacgym

assert isaacgym
import torch
import numpy as np

import glob
import pickle as pkl

from go1_gym.envs import *
from go1_gym.envs.base.legged_robot_config import Cfg
from go1_gym.envs.go1.go1_config import config_go1
from go1_gym.envs.go1.velocity_tracking import VelocityTrackingEasyEnv

from tqdm import tqdm
import pygame
import threading
import time
x_vel = 0
y_vel = 0
z_vel = 0
# 定义手柄读取线程
class JoystickThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        global x_vel, y_vel, z_vel
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
                        if(i==1):
                            x_vel=axis_value
                        elif i == 0:
                            y_vel = axis_value  # 修改全局变量y_vel
                        # 假设z轴是第2个轴，索引为2
                        elif i == 2:
                            z_vel = axis_value  
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

def load_policy(logdir):
    body = torch.jit.load('/home/jiaojunpeng/isaac/RL/walk-these-ways/log_train/1.13-1/body_latest.jit')
    # 假设 body 是您的模型
    print(body)
    import os
    adaptation_module = torch.jit.load('/home/jiaojunpeng/isaac/RL/walk-these-ways/log_train/1.13-1/adaptation_module_latest.jit')

    dummy_input = torch.randn(1, 2102)  # 根据实际情况调整形状

    # 导出 body 模型为 ONNX 格式
    body_onnx_path = '/home/jiaojunpeng/isaac/RL/walk-these-ways/log_train/1.13-1/' + 'body_latest.onnx'
    torch.onnx.export(body, dummy_input, body_onnx_path, opset_version=11)

    # # 导出 adaptation_module 模型为 ONNX 格式
    latent_dummy_input = torch.randn(1, 2100)  # 根据实际情况调整形状
    adaptation_module_onnx_path = '/home/jiaojunpeng/isaac/RL/walk-these-ways/log_train/1.13-1/' + 'adaptation_module_latest.onnx'
    torch.onnx.export(adaptation_module, latent_dummy_input, adaptation_module_onnx_path, opset_version=11)


    def policy(obs, info={}):
        i = 0
        latent = adaptation_module.forward(obs["obs_history"].to('cpu'))
        obs_history = obs["obs_history"]
        # obs["obs_history"]=0
        # print("obsize", obs_history.size())
        # print("obsize",latent.size())
        action = body.forward(torch.cat((obs["obs_history"].to('cpu'), latent), dim=-1))
        info['latent'] = latent
        return action

    return policy


def load_env(label, headless=False):
    dirs = glob.glob(f"../runs/{label}/*")
    logdir = sorted(dirs)[0]

    with open( "/home/jiaojunpeng/isaac/RL/walk-these-ways/log_train/1.9-1/parameters.pkl", 'rb') as file:
        pkl_cfg = pkl.load(file)
        print(pkl_cfg.keys())
        cfg = pkl_cfg["Cfg"]
        print("cfg.keys:",cfg.keys())

        for key, value in cfg.items():
            if hasattr(Cfg, key):
                for key2, value2 in cfg[key].items():
                    setattr(getattr(Cfg, key), key2, value2)
    # Cfg=config_go1
    # turn off DR for evaluation script
    # config_go1(Cfg)
    Cfg.control.stiffness = {'joint': 20.}  # [N*m/rad]
    Cfg.control.damping = {'joint': 0.5}  # [N*m*s/rad]
    Cfg.asset.file= "/home/jiaojunpeng/isaac/RL/walk-these-ways/resources/robots/go2/urdf/go2.urdf"
    Cfg.asset.flip_visual_attachments = True
    Cfg.domain_rand.push_robots = False
    Cfg.domain_rand.randomize_friction = False
    Cfg.domain_rand.randomize_gravity = False
    Cfg.domain_rand.randomize_restitution = False
    Cfg.domain_rand.randomize_motor_offset = False
    Cfg.domain_rand.randomize_motor_strength = False
    Cfg.domain_rand.randomize_friction_indep = False
    Cfg.domain_rand.randomize_ground_friction = False
    Cfg.domain_rand.randomize_base_mass = False
    Cfg.domain_rand.randomize_Kd_factor = False
    Cfg.domain_rand.randomize_Kp_factor = False
    Cfg.domain_rand.randomize_joint_friction = False
    Cfg.domain_rand.randomize_com_displacement = False

    Cfg.env.num_recording_envs = 1
    Cfg.env.num_envs = 1
    Cfg.terrain.num_rows = 5
    Cfg.terrain.num_cols = 5
    Cfg.terrain.border_size = 0
    Cfg.terrain.center_robots = True
    Cfg.terrain.center_span = 1
    Cfg.terrain.teleport_robots = True

    Cfg.domain_rand.lag_timesteps = 6
    Cfg.domain_rand.randomize_lag_timesteps = True
    Cfg.control.control_type = "actuator_net"

    from go1_gym.envs.wrappers.history_wrapper import HistoryWrapper

    env = VelocityTrackingEasyEnv(sim_device='cuda:0', headless=False, cfg=Cfg)
    env = HistoryWrapper(env)

    # load policy
    from ml_logger import logger
    from go1_gym_learn.ppo_cse.actor_critic import ActorCritic

    policy = load_policy(logdir)

    return env, policy


def play_go1(headless=True):
    global x_vel, y_vel, z_vel
    from ml_logger import logger

    from pathlib import Path
    from go1_gym import MINI_GYM_ROOT_DIR
    import glob
    import os

    label = "gait-conditioned-agility/pretrain-v0/train"

    env, policy = load_env(label, headless=headless)

    num_eval_steps = 10000
    gaits = {"pronking": [0, 0, 0],
             "trotting": [0.5, 0, 0],
             "bounding": [0, 0.5, 0],
             "pacing": [0, 0, 0.5]}

    x_vel_cmd, y_vel_cmd, yaw_vel_cmd = x_vel, y_vel, z_vel
    body_height_cmd = 0.0
    step_frequency_cmd = 3.0
    gait = torch.tensor(gaits["trotting"])
    footswing_height_cmd = 0.36
    pitch_cmd = 0.0
    roll_cmd = 0.0
    stance_width_cmd = 0.25

    measured_x_vels = np.zeros(num_eval_steps)
    target_x_vels = np.ones(num_eval_steps) * x_vel_cmd
    joint_positions = np.zeros((num_eval_steps, 12))

    obs = env.reset()

    for i in tqdm(range(num_eval_steps)):
        # with torch.no_grad():
        actions = policy(obs)
        env.commands[:, 0] = 1.5
        env.commands[:, 1] = y_vel
        env.commands[:, 2] = 0
        env.commands[:, 3] = body_height_cmd
        env.commands[:, 4] = step_frequency_cmd
        env.commands[:, 5:8] = gait
        env.commands[:, 8] = 0.5
        env.commands[:, 9] = footswing_height_cmd
        env.commands[:, 10] = pitch_cmd
        env.commands[:, 11] = roll_cmd
        env.commands[:, 12] = stance_width_cmd
        env.commands[:, 13] = pitch_cmd
        env.commands[:, 14] = roll_cmd
        print("envcommands",env.commands[0:12])
        # print("envcommands",env.commands.size())
        obs, rew, done, info = env.step(actions)

        measured_x_vels[i] = env.base_lin_vel[0, 0]
        joint_positions[i] = env.dof_pos[0, :].cpu()

    # plot target and measured forward velocity
    # from matplotlib import pyplot as plt
    # fig, axs = plt.subplots(2, 1, figsize=(12, 5))
    # axs[0].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), measured_x_vels, color='black', linestyle="-", label="Measured")
    # axs[0].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), target_x_vels, color='black', linestyle="--", label="Desired")
    # axs[0].legend()
    # axs[0].set_title("Forward Linear Velocity")
    # axs[0].set_xlabel("Time (s)")
    # axs[0].set_ylabel("Velocity (m/s)")

    # axs[1].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), joint_positions, linestyle="-", label="Measured")
    # axs[1].set_title("Joint Positions")
    # axs[1].set_xlabel("Time (s)")
    # axs[1].set_ylabel("Joint Position (rad)")

    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    # to see the environment rendering, set headless=False
    joystick_thread = JoystickThread()
    joystick_thread.start()
    try:
        play_go1(headless=False)
    except KeyboardInterrupt:
        print("Stopping joystick thread...")
        joystick_thread.stop()
        joystick_thread.join()

