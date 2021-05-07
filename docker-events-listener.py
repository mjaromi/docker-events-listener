import argparse
import datetime
import docker
import sys
import time

events = []
listening_events = ['start', 'stop']

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--timeout', help='Timeout, how long to wait for the next check, in seconds', type=int, default=10, required=False)
    parser.add_argument('-s', '--since', help='Starting point to check events, in seconds', type=int, required=True)
    args = parser.parse_args()

    while True:
        listener(args)
        time.sleep(args.timeout)


def listener(args):
    client = docker.from_env()
    
    until = datetime.datetime.utcnow()
    since = until - datetime.timedelta(seconds=args.since)

    for event in client.events(since=since, until=until, decode=True):
        if event not in events and event['Type'] == 'container':
            events.append(event)
    
    '''
    https://docs.docker.com/engine/api/v1.41/#operation/SystemEvents
    '''
    print('Number of events that have occurred in the last {} seconds that will be processed: {}'.format(args.since, len(events)))
    for index in range(len(events)):
        if events[0]['status'] in listening_events:
            print('Event: {}'.format(events[0]))

        # an additional logic goes here

        del events[0]

    
if __name__== '__main__':
    sys.exit(main())
