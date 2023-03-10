#!/usr/bin/env python3


def main():
    import argparse
    import logging
    import coloredlogs
    from niftiutils import conv16bit, merge16
    import os.path

    logging.basicConfig(format='[%(funcName)s] - %(asctime)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--front', help="front (dorsal) path", metavar="PATH")
    parser.add_argument('-b', '--back', help="back (ventral) path", metavar="PATH")
    parser.add_argument('-o', '--out_path', help="output folder path", default=None, metavar="PATH")
    parser.add_argument('-ms', '--middle_shift', help="shift of the fusion slice", default=0, metavar="# OF SLICES",
                        type=int)
    parser.add_argument('-t', '--thickness', help="thickness of transition (in slices)", default=10,
                        metavar="# OF SLICES")
    parser.add_argument('-c', '--convert', help="convert back to 16 bit (if not already)", action='store_true')
    args = parser.parse_args()

    f_path = args.front
    if args.convert:
        logger.info('converting back image...')
        b_path = conv16bit(args.back)
    else:
        b_path = args.back

    base, filename = os.path.split(args.front)
    name = filename.split('front')[0]
    pattern = "wb_16bit.nii.gz"
    if args.out_path is None:
        out_path = os.path.join(base, name + pattern)
    else:
        out_path = os.path.join(args.out_path, name + pattern)
    logger.info('merging images...')
    merge16(f_path=f_path, b_path=b_path, ms=args.middle_shift, t=args.thickness, out_path=out_path)
    logger.info('done')


if __name__ == "__main__":
    main()
