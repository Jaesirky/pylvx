from _frame import FrameHeader, Frame, DataType, Point0, Point1, Point2, Point3, Point4, Point5, Point6, Package


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

    def __str__(self):
        return 'file_signature'.format(lf.public_header_block.file_signature,
                                       lf.public_header_block.version_a,
                                       lf.public_header_block.version_b,
                                       lf.public_header_block.version_c,
                                       lf.public_header_block.version_d,
                                       lf.public_header_block.magic_code)


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


if __name__ == '__main__':
    lf = LvxFile(r'lvxdemos\2020-10-12 12-12-39.lvx')

    print(asdict(lf))
    print(asdict(lf.public_header_block))
    print(asdict(lf.private_header_block))

    for device in lf.device_info_block:
        device: DeivceInfo
        print(asdict(device))

    for frame in lf.point_data_block:
        frame: Frame
        print(asdict(frame))

        for package in frame.packages:
            package: Package
            print(asdict(package))

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
                elif package.data_type == DataType.IMU_:
                    point: Point6
                else:
                    raise Exception
                print(asdict(point))
