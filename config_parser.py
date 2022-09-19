from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from types import SimpleNamespace

def check_if_val_pos(val, key):
    assert val > -1, "parsing {} failed. make sure values passed are positive (>=0)".format(key)

def check_and_convert_tuple(src, n_elements, key):
    flag = True
    ret = ()
    try:
        ret = tuple((int(x) for x in src.split(",")))
    except ValueError:
        flag = False
    flag = flag and len(ret) == n_elements
    assert flag, "parsing {} failed. check its format".format(key)
    for val in ret:
        check_if_val_pos(val, key)
    return ret

def parse_args():
    parser = ArgumentParser(description = "simple squash-pong game built from python",
            formatter_class = ArgumentDefaultsHelpFormatter)
    default_opts = {}
    default_opts["screen_size"] = [(700, 500), "Screen size fmt:\"w,h\""]
    default_opts["wall_thickness"] = [30, "Wall thickness in pxls"]
    default_opts["ball_radius"] = [10, "Ball's radius in pxls"]
    default_opts["paddle_size"] = [(15, 60), "Paddle size in pxls fmt:\"w,h\""]
    default_opts["score_canvas_height"] = [80, "Score canvas height in pxls"]
    default_opts["screen_color"] = [(0, 0, 0), "Scene background color fmt:\"r,g,b\""]
    default_opts["wall_color"] = [(255, 255, 255), "Wall color fmt:\"r,g,b\""]
    default_opts["ball_color"] = [(255, 0, 0), "Ball color fmt:\"r,g,b\""]
    default_opts["paddle_color"] = [(0, 255, 0), "Paddle color fmt:\"r,g,b\""]
    default_opts["score_color"] = [(0, 127, 127), "Score font color fmt:\"r,g,b\""]
    default_opts["ball_speed"] = [5, "Ball speed in pxls"]
    default_opts["paddle_speed"] = [5, "Paddle speed in pxls"]
    default_opts["font_size"] = [32, "Score font size in pxls"]
    for k,v in default_opts.items():
        type_ = int
        k = "-" + k
        default_ = v[0]
        if isinstance(default_, tuple):
            default_ = ",".join([str(x) for x in default_])
            type_ = str
        parser.add_argument(k, help = v[1], default = default_, type = type_, required = False)
    parser.add_argument("--opencv_display", default = False, action = 'store_true',
            help = "Use opencv's display functions")
    parser.add_argument("--no_score_board", default = False, action = 'store_true',
            help = "Dont display scoreboard")
    parser.add_argument("--no_reset_score", default = False, action = 'store_true',
            help = "Dont reset the score after a loss")
    parser.add_argument("--debug", default = False, action = 'store_true',
            help = "Display debug info")
    args = parser.parse_args()
    args = vars(args)

    # Format check
    for key in default_opts:
        if isinstance(default_opts[key][0], tuple):
            args[key] = check_and_convert_tuple(args[key], len(default_opts[key][0]), key)
        else: # Assuming int type
            check_if_val_pos(args[key], key)

    if args['debug']:
        print('--------------------- SquashPong Config --------------------------')
        for k,v in args.items():
            print('{} = {}'.format(k, v))
        print('------------------------------------------------------------------')

    args = SimpleNamespace(**args)
    return args
