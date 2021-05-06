from autopilot.auto import AutoPilot

import sys
import os
import argparse


path = os.path.realpath(os.path.join(os.getcwd()))
sys.path.insert(0, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='base')
    parser.add_argument('--mode', type=str, default='test')
    args = parser.parse_args()
    ap = AutoPilot(mode=args.mode, model=args.model, debug=True, src=2)
    ap.start()
