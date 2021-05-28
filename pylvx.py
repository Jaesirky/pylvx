import os
from datetime import datetime
from pathlib import Path


def _floatfrombytes(bs):
    import struct
    ans = struct.unpack("!f",bs)[0]
    return ans


class DataType:
    CARTESIAN_MID = 0
    SPHERICAL_MID = 1
    CARTESIAN_SINGLE = 2
    SPHERAICAL_SINGLE = 3
    CARTESIAN_DOUBLE = 4
    SPHERAICAL_DOUBLE = 5
    IMU_INFO = 6


class Point0:
    def __init__(self, bs):
        self.bs = bs

    @property
    def x(self):
        return int.from_bytes(self.bs[:4], 'little', signed=True) 

    @property
    def y(self):
        return int.from_bytes(self.bs[4:8], 'little', signed=True) 

    @property
    def z(self):
        return int.from_bytes(self.bs[8:12], 'little', signed=True) 

    @property
    def reflectivity(self):
        return int.from_bytes(self.bs[12:13], 'little')


class Point1:
    def __init__(self, bs):
        self.bs = bs

    @property
    def depth(self):
        return int.from_bytes(self.bs[:4], 'little', signed=True) 

    @property
    def theta(self):
        return int.from_bytes(self.bs[4:6], 'little')

    @property
    def phi(self):
        return int.from_bytes(self.bs[6:8], 'little')

    @property
    def reflectivity(self):
        return int.from_bytes(self.bs[8:9], 'little')


class Point2:
    def __init__(self, bs):
        self.bs = bs

    @property
    def x(self):
        return int.from_bytes(self.bs[:4], 'little', signed=True) 

    @property
    def y(self):
        return int.from_bytes(self.bs[4:8], 'little', signed=True) 

    @property
    def z(self):
        return int.from_bytes(self.bs[8:12], 'little', signed=True) 

    @property
    def reflectivity(self):
        return int.from_bytes(self.bs[12:13], 'little')

    @property
    def tag(self):
        return int.from_bytes(self.bs[13:14], 'little')


class Point3:
    def __init__(self, bs):
        self.bs = bs

    @property
    def depth(self):
        return int.from_bytes(self.bs[:4], 'little', signed=True) 

    @property
    def theta(self):
        return int.from_bytes(self.bs[4:6], 'little')

    @property
    def phi(self):
        return int.from_bytes(self.bs[6:8], 'little')

    @property
    def reflectivity(self):
        return int.from_bytes(self.bs[8:9], 'little')

    @property
    def tag(self):
        return int.from_bytes(self.bs[9:10], 'little')


class Point4:
    def __init__(self, bs):
        self.bs = bs

    @property
    def x1(self):
        return int.from_bytes(self.bs[:4], 'little', signed=True) 

    @property
    def y1(self):
        return int.from_bytes(self.bs[4:8], 'little', signed=True) 

    @property
    def z1(self):
        return int.from_bytes(self.bs[8:12], 'little', signed=True) 

    @property
    def reflectivity1(self):
        return int.from_bytes(self.bs[12:13], 'little')

    @property
    def tag1(self):
        return int.from_bytes(self.bs[13:14], 'little')

    @property
    def x2(self):
        return int.from_bytes(self.bs[14:18], 'little', signed=True) 

    @property
    def y2(self):
        return int.from_bytes(self.bs[18:22], 'little', signed=True) 

    @property
    def z2(self):
        return int.from_bytes(self.bs[22:26], 'little', signed=True) 

    @property
    def reflectivity2(self):
        return int.from_bytes(self.bs[26:27], 'little')

    @property
    def tag2(self):
        return int.from_bytes(self.bs[27:28], 'little')


class Point5:
    def __init__(self, bs):
        self.bs = bs

    @property
    def theta(self):
        return int.from_bytes(self.bs[:2], 'little')

    @property
    def phi(self):
        return int.from_bytes(self.bs[2:4], 'little')

    @property
    def depth1(self):
        return int.from_bytes(self.bs[4:8], 'little', signed=True) 

    @property
    def reflectivity1(self):
        return int.from_bytes(self.bs[8:9], 'little')

    @property
    def tag1(self):
        return int.from_bytes(self.bs[9:10], 'little')

    @property
    def depth2(self):
        return int.from_bytes(self.bs[10:14], 'little', signed=True) 

    @property
    def reflectivity2(self):
        return int.from_bytes(self.bs[14:15], 'little')

    @property
    def tag2(self):
        return int.from_bytes(self.bs[15:16], 'little')


class Point6:
    def __init__(self, bs):
        self.bs = bs

    @property
    def gyro_x(self):
        return _floatfrombytes(self.bs[:4])

    @property
    def gyro_y(self):
        return _floatfrombytes(self.bs[4:8])

    @property
    def gyro_z(self):
        return _floatfrombytes(self.bs[8:12])

    @property
    def acc_x(self):
        return _floatfrombytes(self.bs[12:16])

    @property
    def acc_y(self):
        return _floatfrombytes(self.bs[16:20])

    @property
    def acc_z(self):
        return _floatfrombytes(self.bs[20:24])


class Package:
    def __init__(self, bs):
        self.bs = bs

    @property
    def device_index(self):
        return int.from_bytes(self.bs[:1], 'little')

    @property
    def version(self):
        return int.from_bytes(self.bs[1:2], 'little')

    @property
    def slot_id(self):
        return int.from_bytes(self.bs[2:3], 'little')

    @property
    def lidar_id(self):
        return int.from_bytes(self.bs[3:4], 'little')

    @property
    def reserved(self):
        return int.from_bytes(self.bs[4:5], 'little')

    @property
    def status_code(self):
        return int.from_bytes(self.bs[5:9], 'little')

    @property
    def timestamp_type(self):
        return int.from_bytes(self.bs[9:10], 'little')

    @property
    def data_type(self):
        return int.from_bytes(self.bs[10:11], 'little')

    @property
    def timestamp(self):
        return int.from_bytes(self.bs[11:19], 'little')

    @property
    def points(self):
        if self.data_type == DataType.CARTESIAN_MID:
            point_size = 13
            point_count = 100
            point_class = Point0
        elif self.data_type == DataType.SPHERICAL_MID:
            point_size = 9
            point_count = 100
            point_class = Point1
        elif self.data_type == DataType.CARTESIAN_SINGLE:
            point_size = 14
            point_count = 96
            point_class = Point2
        elif self.data_type == DataType.SPHERAICAL_SINGLE:
            point_size = 10
            point_count = 96
            point_class = Point3
        elif self.data_type == DataType.CARTESIAN_DOUBLE:
            point_size = 28
            point_count = 48
            point_class = Point4
        elif self.data_type == DataType.SPHERAICAL_DOUBLE:
            point_size = 16
            point_count = 48
            point_class = Point5
        elif self.data_type == DataType.IMU_INFO:
            point_size = 24
            point_count = 1
            point_class = Point6
        else:
            raise Exception
        return [point_class(self.bs[19 + i * point_size: 19 + point_size * (i + 1)]) for i in range(point_count)]


class FrameHeader:
    def __init__(self, bs):
        self.bs = bs

    @property
    def current_offset(self):
        return int.from_bytes(self.bs[:8], 'little')

    @property
    def next_offset(self):
        return int.from_bytes(self.bs[8:16], 'little')

    @property
    def frame_index(self):
        return int.from_bytes(self.bs[16:24], 'little')


class Frame:
    def __init__(self, bs):
        self.bs = bs

    @property
    def frame_header(self):
        return FrameHeader(self.bs[:24])

    @property
    def packages(self):
        current_offset = 24
        while current_offset < len(self.bs):
            pakcage_header = Package(self.bs[current_offset:current_offset + 19])
            if pakcage_header.data_type == DataType.CARTESIAN_MID:
                point_size = 13
                point_count = 100
            elif pakcage_header.data_type == DataType.SPHERICAL_MID:
                point_size = 9
                point_count = 100
            elif pakcage_header.data_type == DataType.CARTESIAN_SINGLE:
                point_size = 14
                point_count = 96
            elif pakcage_header.data_type == DataType.SPHERAICAL_SINGLE:
                point_size = 10
                point_count = 96
            elif pakcage_header.data_type == DataType.CARTESIAN_DOUBLE:
                point_size = 28
                point_count = 48
            elif pakcage_header.data_type == DataType.SPHERAICAL_DOUBLE:
                point_size = 16
                point_count = 48
            elif pakcage_header.data_type == DataType.IMU_INFO:
                point_size = 24
                point_count = 1
            else:
               return
            yield Package(self.bs[current_offset:current_offset + 19 + point_size * point_count])
            current_offset += 19 + point_size * point_count


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
        return _floatfrombytes(bs)

    @property
    def pitch(self):
        bs = self.bs[39:43]
        return _floatfrombytes(bs)

    @property
    def yaw(self):
        bs = self.bs[43:47]
        return _floatfrombytes(bs)

    @property
    def x(self):
        bs = self.bs[47:51]
        return _floatfrombytes(bs)

    @property
    def y(self):
        bs = self.bs[51:55]
        return _floatfrombytes(bs)

    @property
    def z(self):
        bs = self.bs[55:59]
        return _floatfrombytes(bs)


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
            frame_len = frame_header.next_offset - current_offset
            yield Frame(self.fp.read(frame_len))
            current_offset = frame_header.next_offset
            frame_header = FrameHeader(self.fp.read(24))


def asdict(obj):
    d = {}
    for attr in dir(obj):
        if not attr.startswith('__') and not attr.startswith('_'):
            d[attr] = getattr(obj, attr)
    return d


def topcds(lvxfile, outdir, frametime=100):
    def _topcd(frames):
        timestamps = []
        data_type = None
        points = []
        for frame in frames:
            timestamp = 0
            for package in frame.packages:
                package: Package
                if not timestamp:
                    timestamp = package.timestamp
                if data_type is None and package.data_type != DataType.IMU_INFO:
                    data_type = package.data_type
                for point in package.points:
                    if package.data_type == data_type:
                        points.append(point)
            timestamps.append(timestamp)

        timestamp = sum(timestamps) / len(timestamps)
        if data_type not in [DataType.CARTESIAN_SINGLE, DataType.CARTESIAN_DOUBLE]:
            print(data_type)
            return
        filename = datetime.fromtimestamp(timestamp / 10 ** 9).strftime('%Y%m%d%H%M%S%f')
        filepath = os.path.join(outdir, '{}.pcd'.format(filename))
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(filepath):
            f = open(filepath, 'w')
            points_count = len(points) if data_type == DataType.CARTESIAN_SINGLE else 2 * len(points)

            f.write('VERSION 0.7\n')
            f.write('FIELDS x y z reflectivity\n')
            f.write('TYPE F F F U\n')
            f.write('SIZE 4 4 4 1\n')
            f.write('COUNT 1 1 1 1\n')
            f.write('WIDTH {}\n'.format(points_count))
            f.write('HEIGHT 1\n')
            f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
            f.write('POINTS {}\n'.format(points_count))
            f.write('DATA ascii\n')

            for p in points:
                fields = 'x y z reflectivity'.split(' ')
                if data_type == DataType.CARTESIAN_SINGLE:
                    values = [str(getattr(p, field)) for field in fields]
                    f.write(' '.join(values) + '\n')
                else:
                    values = [str(getattr(p, field + '1')) for field in fields]
                    f.write(' '.join(values) + '\n')
                    values = [str(getattr(p, field + '2')) for field in fields]
                    f.write(' '.join(values) + '\n')

            f.close()

    lf = LvxFile(lvxfile)
    duration = lf.private_header_block.frame_duration

    frames = []
    index = 0
    for frame in lf.point_data_block:
        frames.append(frame)
        if (index + 1) % int(frametime / duration) == 0:
            _topcd(frames)
            frames = []
        index += 1
