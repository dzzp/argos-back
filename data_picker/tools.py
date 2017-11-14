import os


def get_origin_path(case_path, img_path):
    img_name = os.path.basename(
        img_path
    ).split('_')[0] + '.jpg'
    origin_path = os.path.join(
        case_path, 'origin', img_name
    )

    return origin_path
