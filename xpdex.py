# File: xpdex.py
# Author: ArctanX
# Date: 2025-06-08

import argparse
import struct
import os
import sys

VERSION = '0.9.0'
COPYRIGHT = "Copyright (c) 2023-2025 ArctanX"

MAX_BANK = 86               # 0-85
VNO_BANK = 96               # vno in bank: 0-95
MAX_VNO = 8256              # 0-8255
BYTEORDER = 'big'
READ_BINARY = 'rb'
WRITE_BINARY = 'wb'
EXT_PDX_LC = '.pdx'
EXT_PDX_UC = '.PDX'


# ----------------------------------------------------------------------------
def main():
    args = parse_args()
    opt_v = args.verbose

    pdx = Pdx(args.pdx_fname)
    if pdx.get_filesize(opt_v):
        if pdx.get_header(args):
            if pdx.extract_pcm(args):
                v_print(1, "Completed.", opt_v)


# ----------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description='Extract PCM file(s) from a PDX file.', epilog=COPYRIGHT)
    parser.add_argument('pdx_fname', metavar='PDX_filename',
                        help='specify PDX filename')
    parser.add_argument('pcm_num', nargs='*', type=int,
                        help='specify PCM number to extract (0-8255)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force to overwrite pcm file(s)')
    parser.add_argument('-p', '--prefix', dest='prefix', nargs='?', const='',
                        help='specify prefix of PCM files')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase verbose level')
    parser.add_argument('-V', '--version', action='version',
                        version=f'%(prog)s {VERSION}')
    args = parser.parse_args()
    v_print(3, args, args.verbose)
    return args


# ----------------------------------------------------------------------------
def v_print(verbose_level, message, opt_v):
    if verbose_level <= opt_v:
        print(message)
    return


# ----------------------------------------------------------------------------
class Pdx:
    def __init__(self, filename) -> None:
        self.fname = filename
        self.fname_bname = os.path.splitext(os.path.basename(self.fname))[0]
        self.fsize = 0
        self.last_bank = 0          # 0-85
        self.pcm_ptrlen = {}

    def get_filesize(self, opt_v):
        if not os.access(self.fname, os.R_OK):
            v_print(4, f'{self.fname} not found.', opt_v)
            if os.access(self.fname + EXT_PDX_LC, os.R_OK):
                v_print(4, f'{self.fname + EXT_PDX_LC} found.', opt_v)
                self.fname += EXT_PDX_LC
            elif os.access(self.fname + EXT_PDX_UC, os.R_OK):
                v_print(4, f'{self.fname + EXT_PDX_UC} found.', opt_v)
                self.fname += EXT_PDX_UC
            else:
                print(f'{self.fname} / {self.fname + EXT_PDX_LC} / '
                      f'{self.fname + EXT_PDX_UC} cannot be opened.',
                      file=sys.stderr)
                return False
        self.fsize = os.path.getsize(self.fname)
        v_print(3, f'{self.fname} size = {self.fsize}', opt_v)
        return True

    def get_header(self, args):
        fmt = ">2L"
        data_size = struct.calcsize(fmt)
        end_vno = last_vno = tmp_vno = MAX_VNO - 1
        is_success = True
        opt_v = args.verbose

        with open(self.fname, READ_BINARY) as f:
            for vno in range(MAX_VNO):
                v_print(4, f'end_vno = {end_vno}, last_vno = {last_vno},'
                        f' tmp_vno = {tmp_vno}', opt_v)
                try:
                    pcm_info = struct.unpack(fmt, f.read(data_size))
                except Exception as e:
                    v_print(4, e, opt_v)
                    is_success = False
                    break
                if pcm_info[0]+pcm_info[1] > self.fsize:
                    v_print(4,
                            f'Offset({pcm_info[0]:,})'
                            f' + Length({pcm_info[1]:,})'
                            f' = {pcm_info[0]+pcm_info[1]:,}'
                            f' > filesize({self.fsize:,})', opt_v)
                    is_success = False
                    break
                if pcm_info[0] != 0:
                    self.pcm_ptrlen[vno] = [pcm_info[0], pcm_info[1]]
                    last_vno = vno
                    tmp_vno = pcm_info[0] // data_size - 1
                    if tmp_vno < 0:
                        is_success = False
                        break
                    if tmp_vno < end_vno:
                        v_print(3, f'end_vno : {end_vno} -> {tmp_vno}', opt_v)
                        end_vno = tmp_vno
                if vno >= end_vno:
                    v_print(3, f'vno ({vno}) >= end_vno ({end_vno})', opt_v)
                    break
            v_print(3, f'last_vno = {last_vno}', opt_v)
            if ((end_vno + 1) // VNO_BANK >= 2) or (last_vno >= VNO_BANK):
                self.last_bank = end_vno // VNO_BANK
            else:
                self.last_bank = last_vno // VNO_BANK

        if is_success:
            self.__print_pdx_header(args, 2)
            v_print(3, f'self.last_bank = {self.last_bank}', opt_v)
        else:
            v_print(1, 'This file seems to be broken as PDX-file.', opt_v)
        return is_success

    def __print_pdx_header(self, args, level):
        if level <= args.verbose:
            print('-------+------------+------------')
            print(' PCM # |   Offset   |   Length   ')
            print('=======+============+============')
            for vno, ptrlen in self.pcm_ptrlen.items():
                if (not args.pcm_num) or (vno in args.pcm_num):
                    print(' %05d | %10d | %10d ' % (vno, ptrlen[0], ptrlen[1]))
            print('-------+------------+------------')
        return

    def __mk_pcm_fname(self, args, vno):
        pcm_fname = ''
        if args.prefix is not None:
            if args.prefix == '':
                pcm_fname = f'{self.fname_bname}_'
            else:
                pcm_fname = args.prefix
        if self.last_bank == 0:
            pcm_fname += '%02d.pcm' % vno
        else:
            pcm_fname += '%05d.pcm' % vno
        return pcm_fname

    def extract_pcm(self, args):
        pcm_fname = ''
        is_success = True
        with open(self.fname, READ_BINARY) as f:
            for vno in self.pcm_ptrlen.keys():
                try:
                    if (not args.pcm_num) or (vno in args.pcm_num):
                        f.seek(self.pcm_ptrlen[vno][0])
                        pcm_fname = self.__mk_pcm_fname(args, vno)
                        pcm = Pcm(pcm_fname)
                        pcm.writedata(f.read(self.pcm_ptrlen[vno][1]),
                                      args.force, args.verbose)
                except Exception as e:
                    v_print(4, e, args.verbose)
                    v_print(1, 'Extraction Error: pcm_fname', args.verbose)
                    is_success = False
        return is_success


# ----------------------------------------------------------------------------
class Pcm:
    def __init__(self, filename) -> None:
        self.fname = filename

    def __chk_overwrite(self):
        if os.path.exists(self.fname):
            choice = input('[WARNING] %s already exists - overwrite? '
                           '[y/Other] ' % self.fname).lower()
            if choice != 'y':
                return False
        return True

    def writedata(self, data, opt_f, opt_v):
        if opt_f or self.__chk_overwrite():
            with open(self.fname, WRITE_BINARY) as f:
                written_b = f.write(data)
                v_print(1,
                        f'extracted {self.fname} : {written_b} bytes.',
                        opt_v)
        else:
            v_print(2, f'Not overwritten: {self.fname}', opt_v)
        return


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
