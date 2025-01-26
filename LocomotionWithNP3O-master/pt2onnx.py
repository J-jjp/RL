# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

import math
import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import torch
from modules.actor_critic import ActorCriticMixedBarlowTwins
import torch.nn as nn

ROOT_DIR = os.path.dirname(__file__)
ENVS_DIR = os.path.join(ROOT_DIR,'Env')


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Deployment script.')
    parser.add_argument('--load_model', type=str, default='/home/jjp/issac/RL/LocomotionWithNP3O-master/go1.pt',
                        help='Run to load from.')
    parser.add_argument('--terrain', action='store_true', default=False)
    args = parser.parse_args()

    model = torch.load(args.load_model)# 有一个可能得原因是这个 pt文件里只有权重，而没有网络结构。 所以 只能用 torch.load去加载，不能用torch.jit.load
    model.eval()
    model.float()

    args = {
        'continue_from_last_std': True,
        'imi_flag': False,
        'num_costs': 9,
        'priv_encoder_dims': [],
        'rnn_hidden_size': 512,
        'rnn_num_layers': 1,
        'rnn_type': 'lstm',
        'tanh_encoder_output': False,
        'teacher_act': False
    }

    actor_critic = ActorCriticMixedBarlowTwins(45,187,736,54,10,12,
                                               [128,64,32,],
                                      [512,256,128],
                                      [512,256,128],
                                      'elu',
                                      1.0,**args)

    model = model.state_dict()
    actor_critic.load_state_dict(model)

 
 # Let's create a dummy input tensor  
    #dummy_input = torch.randn(1, 3, 32, 32, requires_grad=True)
    obs = torch.rand(736).unsqueeze(0)
    # Export the model   
    torch.onnx.export(actor_critic,         # model being run
        obs,     # model input (or a tuple for multiple inputs)
         "bset1.onnx")
    print(" ") 
    print('Model has been converted to ONNX') 