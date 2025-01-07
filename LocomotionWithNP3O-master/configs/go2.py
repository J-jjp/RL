# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from configs.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO


class go2(LeggedRobotCfg):
    class env(LeggedRobotCfg.env):
        num_envs = 4096  # 1024

        n_scan = 187
        n_priv_latent = 4 + 1 + 12 + 12 + 12 + 6 + 1 + 4 + 1 - 3 + 4
        n_proprio = 45  # 原始观测
        history_len = 10
        num_observations = n_proprio + n_priv_latent + n_scan + history_len * n_proprio
        amao = 1

        en_logger = False  # wanda

    class init_state(LeggedRobotCfg.init_state):
        pos = [0.0, 0.0, 0.43]  # x,y,z [m]
        """Dof order:
            FL_hip_joint
            FL_thigh_joint
            FL_calf_joint
            FR_hip_joint
            FR_thigh_joint
            FR_calf_joint
            RL_hip_joint
            RL_thigh_joint
            RL_calf_joint
            RR_hip_joint
            RR_thigh_joint
            RR_calf_joint
        """
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            'FL_hip_joint': 0.1,   # [rad]
            'RL_hip_joint': 0.1,   # [rad]
            'FR_hip_joint': -0.1 ,  # [rad]
            'RR_hip_joint': -0.1,   # [rad]

            'FL_thigh_joint': 0.8,     # [rad]
            'RL_thigh_joint': 0.8,   # [rad]
            'FR_thigh_joint': 0.8,     # [rad]
            'RR_thigh_joint': 0.8,   # [rad]

            'FL_calf_joint': -1.5,   # [rad]
            'RL_calf_joint': -1.5,    # [rad]
            'FR_calf_joint': -1.5,  # [rad]
            'RR_calf_joint': -1.5,    # [rad]
        }

    # stiffness = {'leg_roll': 200.0, 'leg_pitch': 350.0, 'leg_yaw': 200.0,
    #                 'knee': 350.0, 'ankle': 15}
    # damping = {'leg_roll': 10, 'leg_pitch': 10, 'leg_yaw':
    #             10, 'knee': 10, 'ankle': 10}  关节名字可以区分，mujoco下与其一致
    class control(LeggedRobotCfg.control):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 30}  # [N*m/rad]
        damping = {'joint': 0.75}  # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        hip_scale_reduction = 1

        use_filter = True

    class commands(LeggedRobotCfg.control):
        curriculum = False
        max_curriculum = 1.
        num_commands = 4  # default: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        resampling_time = 10.  # time before command are changed[s]W
        heading_command = True  # if true: compute ang vel command from heading error
        global_reference = False

        class ranges:
            lin_vel_x = [-1.0, 1.0]  # min max [m/s]
            lin_vel_y = [-1.0, 1.0]  # min max [m/s]
            ang_vel_yaw = [-1.0, 1.0]  # min max [rad/s]
            heading = [-3.14, 3.14]
            height = [0.12, 0.2]  # m

    class asset(LeggedRobotCfg.asset):
        file = '{ROOT_DIR}/resources/go2/urdf/go2.urdf'
        foot_name = "foot"  # URDF需要具有foot的link
        name = "go2_description"
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = ["base"]
        self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = True  # tinymal

    class rewards(LeggedRobotCfg.rewards):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.4
        clearance_height_target = -0.2 # 相对站立高度 不能和高度差距太大
        tracking_sigma = 0.35  # 0.25 小了探索出来爬行 300  0.15 小惯量  0.25 大惯量

        cycle_time = 0.5  # s
        touch_thr = 5  # N
        command_dead = 0.1
        target_joint_pos_scale = 0.17  # rad

        max_contact_force = 150  # N

        class scales(LeggedRobotCfg.rewards.scales):
            torques = 0.0
            powers = -2e-5
            termination = 0.0
            tracking_lin_vel = 1.0
            tracking_ang_vel = 0.5
            base_acc = -0.02
            lin_vel_z = -2.0
            ang_vel_xy = -0.05
            dof_vel = 0.0
            dof_acc = -2e-7
            base_height = -1.0

            collision = 0.0
            feet_stumble = 0.0
            action_rate = -0.01
            action_smoothness = -0.01
            stand_still = -0.01

            feet_air_time = 1
            foot_clearance = -1
            # no_fly  =0.005
            orientation_eular = 0.15  # 0.05可以探索爬行
            # default_joint_pos=-0.02
            # joint_ref_pos =0.505
            # feet_contact_number=-1
            hip_pos = -0.5

            feet_contact_forces = -0.01
            vel_mismatch_exp = 0.3  # lin_z; ang x,y  速度奖励大可以鼓励机器人更多移动，与摆腿耦合
            low_speed = 0.2
            track_vel_hard = 0.5
            foot_slip = -0.05

    class domain_rand(LeggedRobotCfg.domain_rand):
        randomize_friction = True
        friction_range = [0.2, 2.75]
        randomize_restitution = True
        restitution_range = [0.0, 1.0]
        randomize_base_mass = True
        added_mass_range = [-1, 3]
        randomize_base_com = True
        added_com_range = [-0.03, 0.03]
        push_robots = True
        push_interval_s = 15
        max_push_vel_xy = 1

        randomize_motor = True
        motor_strength_range = [0.8, 1.2]  # 比例系数

        randomize_kpkd = True
        kp_range = [0.8, 1.2]  # 比例系数
        kd_range = [0.8, 1.2]

        randomize_lag_timesteps = True
        lag_timesteps = 6

    class depth(LeggedRobotCfg.depth):
        use_camera = False
        camera_num_envs = 192
        camera_terrain_num_rows = 10
        camera_terrain_num_cols = 20

        position = [0.27, 0, 0.03]  # front camera
        angle = [-5, 5]  # positive pitch down

        update_interval = 1  # 5 works without retraining, 8 worse

        original = (106, 60)
        resized = (87, 58)
        horizontal_fov = 87
        buffer_len = 2

        near_clip = 0
        far_clip = 2
        dis_noise = 0.0

        scale = 1
        invert = True

    class costs:
        class scales:
            pos_limit = 0.1
            torque_limit = 0.1
            dof_vel_limits = 0.1
            feet_air_time = 0.1
            acc_smoothness = 0.1
            collision = 0.1
            stand_still = 0.1  # 站立默认位置
            hip_pos = 0.1  # 侧展
            base_height = 0.1
            # foot_regular = 0.1
            # trot_contact = 0.1

        class d_values:
            pos_limit = 0.0
            torque_limit = 0.0
            dof_vel_limits = 0.0
            feet_air_time = 0.1
            acc_smoothness = 0.0
            collision = 0.0
            stand_still = 0.0
            hip_pos = 0.0
            base_height = 0.0
            # foot_regular = 0.0
            # trot_contact = 1

    class cost:
        num_costs = 9  # 需要同步修改 policy

    class terrain(LeggedRobotCfg.terrain):
        mesh_type = 'trimesh'  # "heightfield" # none, plane, heightfield or trimesh
        measure_heights = True
        include_act_obs_pair_buf = False


class go2PPO(LeggedRobotCfgPPO):
    class algorithm(LeggedRobotCfgPPO.algorithm):
        # entropy_coef = 0.01
        # learning_rate = 1.e-3
        # max_grad_norm = 1
        # num_learning_epochs = 5
        # num_mini_batches = 4 # mini batch size = num_envs*nsteps / nminibatches
        # cost_value_loss_coef = 0.1
        # cost_viol_loss_coef = 1

        # entropy_coef = 0.001
        # learning_rate = 1e-5
        # num_learning_epochs = 2
        # gamma = 0.994
        # lam = 0.9
        # num_mini_batches = 4

        value_loss_coef = 1.0
        use_clipped_value_loss = True
        clip_param = 0.2
        entropy_coef = 0.001
        num_learning_epochs = 5
        num_mini_batches = 4  # minibatch size = num_envs*nsteps/nminibatches
        learning_rate = 1.e-4
        schedule = 'adaptive'  # could be adaptive, fixed
        gamma = 0.98
        lam = 0.95
        desired_kl = 0.01
        max_grad_norm = 1.
        weight_decay = 0

    class policy(LeggedRobotCfgPPO.policy):
        init_noise_std = 1.0
        continue_from_last_std = True
        scan_encoder_dims = [128, 64, 32]
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]
        # priv_encoder_dims = [64, 20]
        priv_encoder_dims = []
        activation = 'elu'  # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid
        # only for 'ActorCriticRecurrent':
        rnn_type = 'lstm'
        rnn_hidden_size = 512
        rnn_num_layers = 1

        tanh_encoder_output = False
        num_costs = 9  # 需要同步修改

        teacher_act = False
        imi_flag = False

    class runner(LeggedRobotCfgPPO.runner):
        run_name = 'test_barlowtwins'
        experiment_name = 'rough_go2_constraint'
        policy_class_name = 'ActorCriticMixedBarlowTwins'
        runner_class_name = 'OnConstraintPolicyRunner'
        algorithm_class_name = 'NP3O'
        max_iterations = 4000  # 最大训练回合
        save_interval = 1000  # 保存周期
        num_steps_per_env = 24
        resume = False
        resume_path = '/home/pi/Downloads/LocomotionWithNP3O-master/logs/rough_go2_constraint/Aug01_23-04-52_test_barlowtwins/model_1000.pt'



