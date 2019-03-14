import time
import os
import torch
import argparse
from auto_schedule.examples import FUNC_TABLE
from auto_schedule.test import test_graph_schedule_cpu_general_dx
from auto_schedule.train import Entity, train_op_schedule_cpu_general_dx


def run(test=False):
    entities = []
    func = FUNC_TABLE["conv2d_channel_batch"].func
    args = (1, 14, 14, 256, 3, 3, 512, 1, 1)
    entities.append(Entity(func, args))
    model_path = os.path.abspath("../models/opt_conv1_cpu.pkl")
    if not test:
        beg = time.time()
        train_op_schedule_cpu_general_dx(entities, 5, 16, model_path)
        end = time.time()
        print("{}({}):".format("conv2d_channel_batch", args))
        print("train done! use {}ms".format((end - beg) * 1e3))
    test_graph_schedule_cpu_general_dx(func, args, model_path)


def pytorch_baseliine():
    conv = torch.nn.Conv2d(256, 512, (3, 3), (1, 1), (1, 1), bias=False)
    A = torch.rand([1, 256, 14, 14])
    beg = time.time()
    for i in range(100):
        out = conv(A)
    end = time.time()
    print("pytorch use {}ms".format((end - beg) / 100 * 1e3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train", help="train the model", action="store_true")
    parser.add_argument("-p", "--pytorch", help="run pytorch baseline", action="store_true")
    parser.add_argument("-a", "--auto_schedule", help="run auto-scheduler", action="store_true")
    args = parser.parse_args()
    test = not args.train
    use_torch = args.pytorch
    use_auto = args.auto_schedule
    if use_torch:
        pytorch_baseliine()
    if use_auto:
        run(test)