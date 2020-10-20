from pylvx import *
from _frame import *

lf = LvxFile(r'lvxdemos\2020-10-12 12-12-39.lvx')

# print(asdict(lf))
# print(asdict(lf.public_header_block))
# print(asdict(lf.private_header_block))

for device in lf.device_info_block:
    device: DeivceInfo
    print(asdict(device))

for frame in lf.point_data_block:
    frame: Frame
    # print(asdict(frame))

    for package in frame.packages:
        package: Package
        # print(asdict(package))
        for point in package.points:
            if package.data_type == DataType.CARTESIAN_MID:
                point: Point0
            elif package.data_type == DataType.SPHERICAL_MID:
                point: Point1
            elif package.data_type == DataType.CARTESIAN_SINGLE:
                point: Point2
            elif package.data_type == DataType.SPHERAICAL_SINGLE:
                point: Point3
            elif package.data_type == DataType.CARTESIAN_DOUBLE:
                point: Point4
            elif package.data_type == DataType.SPHERAICAL_DOUBLE:
                point: Point5
            elif package.data_type == DataType.IMU_INFO:
                point: Point6
            else:
                raise Exception
            # print(asdict(point))
