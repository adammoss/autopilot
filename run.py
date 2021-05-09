from autopilot.auto import AutoPilot

import sys
import os
import argparse
import time


path = os.path.realpath(os.path.join(os.getcwd()))
sys.path.insert(0, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='base')
    parser.add_argument('--mode', type=str, default='test')
    parser.add_argument('--capture_src', type=int, default=0)
    parser.add_argument('--picar_config', type=str, default='')
    parser.add_argument('--duration', type=int, default=300)
    parser.add_argument('--max_speed', type=int, default=35)
    args = parser.parse_args()
    front_wheels = None
    back_wheels = None
    if args.mode == 'drive':
        try:
            import picar
            picar.setup()
            front_wheels = picar.front_wheels.Front_Wheels(debug=False, db=args.picar_config)
            back_wheels = picar.back_wheels.Back_Wheels(debug=False, db=args.picar_config)
            front_wheels.ready()
            back_wheels.ready()
        except ModuleNotFoundError:
            print('[!] Cannot setup picar, have you installed it?')

    ap = AutoPilot(front_wheels=front_wheels, back_wheels=back_wheels,
                   mode=args.mode, model=args.model, debug=True, capture_src=args.capture_src,
                   max_speed=args.max_speed)
    ap.start()
    time.sleep(args.duration)
    ap.stop()
