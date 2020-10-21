from ._frame import FrameHeader, Frame, DataType, Point0, Point1, Point2, Point3, Point4, Point5, Point6, Package
import os
from datetime import datetime

class PublicHeader:
    def __init__(self, bs):
        self.bs = bs

    @property
    def file_signature(self):
        return self.bs[:16].decode()

    @property
    def version_a(self):
        return int.from_bytes(self.bs[16:17], 'little')

    @property
    def version_b(self):
        return int.from_bytes(self.bs[17:18], 'little')

    @property
    def version_c(self):
        return int.from_bytes(self.bs[18:19], 'little')

    @property
    def version_d(self):
        return int.from_bytes(self.bs[19:20], 'little')

    @property
    def magic_code(self):
        # ? 无符号是否这样转
        return int.from_bytes(self.bs[20:24], 'little')


class PrivateHeader:
    def __init__(self, bs):
        self.bs = bs

    @property
    def frame_duration(self):
        return int.from_bytes(self.bs[:4], 'little')

    @property
    def device_count(self):
        return int.from_bytes(self.bs[4:5], 'little')


class DeivceInfo:
    def __init__(self, bs):
        self.bs: bytes = bs

    @property
    def lidar_sn_code(self):
        return self.bs[:16].decode()

    @property
    def hub_sn_code(self):
        return self.bs[16:32].decode()

    @property
    def device_index(self):
        return int.from_bytes(self.bs[32:33], 'little')

    @property
    def device_type(self):
        return int.from_bytes(self.bs[33:34], 'little')

    @property
    def extrinsic_enable(self):
        return int.from_bytes(self.bs[34:35], 'little')

    @property
    def roll(self):
        bs = self.bs[35:39]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)

    @property
    def pitch(self):
        bs = self.bs[39:43]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)

    @property
    def yaw(self):
        bs = self.bs[43:47]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)

    @property
    def x(self):
        bs = self.bs[47:51]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)

    @property
    def y(self):
        bs = self.bs[51:55]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)

    @property
    def z(self):
        bs = self.bs[55:59]
        hs = ''.join(['%02X' % x for x in bs])
        return float.fromhex(hs)


class LvxFile:
    def __init__(self, fp):
        self.fp = open(fp, 'rb')

    @property
    def public_header_block(self):
        self.fp.seek(0)
        return PublicHeader(self.fp.read(24))

    @property
    def private_header_block(self):
        self.fp.seek(24)
        return PrivateHeader(self.fp.read(5))

    @property
    def device_info_block(self):
        self.fp.seek(29)
        for _ in range(self.private_header_block.device_count):
            yield DeivceInfo(self.fp.read(59))

    @property
    def point_data_block(self):
        current_offset = 29 + 59 * int(self.private_header_block.device_count)
        self.fp.seek(current_offset)
        frame_header = FrameHeader(self.fp.read(24))
        assert frame_header.current_offset == current_offset

        while frame_header.next_offset:
            self.fp.seek(current_offset)
            yield Frame(self.fp.read(frame_header.next_offset - current_offset))
            current_offset = frame_header.next_offset
            frame_header = FrameHeader(self.fp.read(24))


def asdict(obj):
    d = {}
    for attr in dir(obj):
        if not attr.startswith('__') and not attr.startswith('_'):
            d[attr] = getattr(obj, attr)
    return d


def topcds(lvxfile, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    lf = LvxFile(lvxfile)

    index = 0
    for frame in lf.point_data_block:
        timestamp = 0
        data_type = None
        points = []
        for package in frame.packages:
            package: Package
            if not timestamp:
                timestamp = package.timestamp
            if data_type is None and package.data_type != DataType.IMU_INFO:
                data_type = package.data_type
            for point in package.points:
                if package.data_type == data_type:
                    points.append(point)
        f = open(os.path.join(outdir, '{}.pcd'.format(datetime.fromtimestamp(timestamp/10**9).strftime('%Y%m%d%H%M%S%f'))), 'w')

        f.write('VERSION 0.7\n')
        if data_type == DataType.CARTESIAN_MID:
            field_line = "FIELDS x y z reflectivity"
            type_line = "TYPE I I I U"
            size_line = "SIZE 4 4 4 1"
            count_line = "COUNT 1 1 1 1"
        elif data_type == DataType.SPHERICAL_MID:
            field_line = "FIELDS theta phi depth reflectivity"
            type_line = "TYPE U U I U"
            size_line = "SIZE 2 2 4 1"
            count_line = "COUNT 1 1 1 1"
        elif data_type == DataType.CARTESIAN_SINGLE:
            field_line = "FIELDS x y z reflectivity tag"
            type_line = "TYPE I I I U U"
            size_line = "SIZE 4 4 4 1 1"
            count_line = "COUNT 1 1 1 1 1"
        elif data_type == DataType.SPHERAICAL_SINGLE:
            field_line = "FIELDS theta phi depth reflectivity tag"
            type_line = "TYPE U U I U U"
            size_line = "SIZE 2 2 4 1 1"
            count_line = "COUNT 1 1 1 1 1"
        elif data_type == DataType.CARTESIAN_DOUBLE:
            field_line = "FIELDS x1 y1 z1 reflectivity1 tag1 x2 y2 z2 reflectivity2 tag2"
            type_line = "TYPE I I I U U I I I U U"
            size_line = "SIZE 4 4 4 1 1 4 4 4 1 1"
            count_line = "COUNT 1 1 1 1 1 1 1 1 1 1"
        elif data_type == DataType.SPHERAICAL_DOUBLE:
            field_line = "FIELDS theta phi depth1 reflectivity1 tag1 depth2 reflectivity2 tag2"
            type_line = "TYPE U U I U U I U U"
            size_line = "SIZE 2 2 4 1 1 4 1 1"
            count_line = "COUNT 1 1 1 1 1 1 1 1"
        else:
            raise

        f.write(field_line + '\n')
        f.write(size_line + '\n')
        f.write(type_line + '\n')
        f.write(count_line + '\n')
        f.write('WIDTH {}\n'.format(len(points)))
        f.write('HEIGHT 1\n')
        f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
        f.write('POINTS {}\n'.format(len(points)))
        f.write('DATA ascii\n')

        for p in points:
            fields = field_line.split(' ')[1:]
            values = [str(getattr(p, field)) for field in fields]
            f.write(' '.join(values) + '\n')
        f.close()
        index+=1
