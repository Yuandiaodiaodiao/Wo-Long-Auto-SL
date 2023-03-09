import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--width', type=int, help='屏幕宽度', default=3840)
parser.add_argument('--height', type=int, help='屏幕高度', default=2160)
parser.add_argument('--mode', type=str, help='显示模式 全屏 无边框 窗口', default="borderless")
parser.add_argument('--scale', type=int, help='系统缩放倍率', default="2")
args = parser.parse_args()
