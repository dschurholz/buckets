#! /usr/bin/env python
"""
A python script that simulates the token bucket and leaky bucket algorithms for
flow control in computer networks.
"""
from __future__ import print_function
import sys
import argparse
import time


ACCEPTED = 'ACCEPTED'
REJECTED = 'REJECTED'
SENT = 'SENT'


class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def leaky_bucket(r, size, packet_size, time_lapse, packet_dates):
    bucket = 0
    leak = 0
    sent_data = []
    queue = 0
    sent_packets = 0
    r = r / 1000.0  # Converting r to milliseconds
    for i in xrange(0, time_lapse + 1):
        flag = 0
        if i in packet_dates:
            queue += 1
            bucket += packet_size
            flag = 1

        if bucket > size and queue > 0:
            queue -= 1
            bucket -= packet_size
            sent_data.append([i, bucket, REJECTED, sent_packets, leak, queue])
        elif leak >= packet_size:
            leak = 0
            queue -= 1
            sent_packets += 1
            sent_data.append([i, bucket, SENT, sent_packets, leak, queue])
        else:
            if not flag:
                sent_data.append([
                    i, bucket, '--------', sent_packets, leak, queue])
            else:
                sent_data.append([
                    i, bucket, ACCEPTED, sent_packets, leak, queue])

        bucket -= r

        if queue > 0:
            leak += r
        elif queue == 0:
            leak = 0

        if bucket < 0:
            bucket = 0

    return (sent_packets, sent_data)


def token_bucket(r, size, input_rate, packet_size, time_lapse, packet_dates):
    bucket = size
    burst_period = float(float(size) / float(input_rate - r))
    burst_size = input_rate * burst_period
    sent_data = []
    sent_packets = 0
    r = r / 1000.0  # Converting r to milliseconds
    for i in xrange(0, time_lapse + 1):
        if i in packet_dates:
            if bucket < packet_size:
                sent_data.append([i, bucket, REJECTED, sent_packets])
            else:
                bucket -= packet_size
                sent_packets += 1
                sent_data.append([i, bucket, SENT, sent_packets])
        else:
            sent_data.append([i, bucket, '--------', sent_packets])

        bucket += r
        if bucket > size:
            bucket = size

    return (sent_packets, sent_data, burst_period, burst_size)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--leaky", default=False, action="store_true",
        help="set the bucket to leaky")

    parser.add_argument(
        "--bucket-size", type=float, default=5000.0, dest='bucket_size',
        help="set the bucket size (in bytes) (default 5KB)")

    parser.add_argument(
        "--input-rate", type=float, default=10000000.0, dest='input_rate',
        help="the rate at which packages arrive (in bytes per second) (default 10MB/s)")

    parser.add_argument(
        "--rate", type=float, default=100000.0,
        help="the rate at which tokens arrive to the bucket (in bytes per second) (default 100KB/s)")

    parser.add_argument(
        "--packet-size", type=float,  default=1000.0, dest='packet_size',
        help="the size of each incoming packet (in bytes) (default 1KB)")

    parser.add_argument(
        "--time-lapse", type=int, default=100, dest='time_lapse',
        help="the time_lapse in which the bucket functions (in millisecond) (default 100ms)")

    parser.add_argument(
        "--exec-speed", type=float, default=0.5, dest='exec_speed',
        help="the execution speed of the simulation (in seconds) (default 0.5seconds/millisecond)")

    # Set the packet array:
    p_array = [1, 2, 3, 4, 5, 6, 30, 34, 36, 38, 50, 60, 80, 82, 84, 86,
               88, 100]
    parser.add_argument(
        '--packet-dates', nargs='+', default=p_array, dest='packet_dates',
        type=int,
        help='Set of packet dates in milliseconds (default %s)' % p_array)

    args = parser.parse_args()

    print (args.packet_dates)
    if args.input_rate < args.rate:
        print(bcolors.FAIL,
              "The bucket token rate must be lower than the incomming" +
              " traffic rate.", bcolors.ENDC)
    elif not args.leaky:
        sent_packets, sent_data, burst_period, burst_size = (
            token_bucket(
                args.rate, args.bucket_size, args.input_rate, args.packet_size,
                args.time_lapse, args.packet_dates)
        )

        print("=" * 60)
        print("Time | Bucket | Status | Number of Packs Sent")
        print("=" * 60)
        for data in sent_data:
            if data[2] == SENT:
                print(
                    bcolors.OKBLUE, str(data[0]) + 'ms', '|', data[1], '|  ',
                    data[2], '  |', data[3], bcolors.ENDC)

            elif data[2] == REJECTED:
                print(bcolors.FAIL, str(data[0]) + 'ms', '|', data[1], '|',
                      data[2], '|', data[3], bcolors.ENDC)

            else:
                print('', str(data[0]) + 'ms', '|', data[1], '|',
                      data[2], '|', data[3])
            time.sleep(args.exec_speed)

        print("\nSENT PACKETS:", sent_packets)
        print("BURST SIZE (in KB):", round(burst_size, 2))
        print("BURST PERIOD (in seconds):", round(burst_period, 6))
        print("=" * 60)

    elif args.leaky:
        sent_packets, sent_data = (
            leaky_bucket(
                args.rate, args.bucket_size, args.packet_size,
                args.time_lapse, args.packet_dates)
        )

        print("=" * 60)
        print("Time | Bucket | Status | Number of Packs Sent | Leack | Queue")
        print("=" * 60)
        for data in sent_data:
            if data[2] == SENT:
                print(bcolors.OKBLUE, str(data[0]) + 'ms', '|', data[1], '|  ',
                      data[2], '  |', data[3], '|', data[4], '|', data[5],
                      bcolors.ENDC)

            elif data[2] == REJECTED:
                print(bcolors.FAIL, str(data[0]) + 'ms', '|', data[1], '|',
                      data[2], '|', data[3], '|', data[4], '|', data[5],
                      bcolors.ENDC)

            elif data[2] == ACCEPTED:
                print(bcolors.OKGREEN, str(data[0]) + 'ms', '|', data[1], '|',
                      data[2], '|', data[3], '|', data[4], '|', data[5],
                      bcolors.ENDC)

            else:
                print('', str(data[0]) + 'ms', '|', data[1], '|',
                      data[2], '|', data[3], '|', data[4], '|', data[5])
            time.sleep(args.exec_speed)

        print("\nSENT PACKETS:", sent_packets)
        print("=" * 60)

if __name__ == "__main__":
    main()
