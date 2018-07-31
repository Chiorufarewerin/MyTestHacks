from MyTest import StartProgram
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-host",help="Host to MyTestServer (ip or name of pc)")
    parser.add_argument("-port",help="Port to MyTestServer",type=int)
    parser.add_argument("-err",help="Count errors (if you want)",type=int)
    args = parser.parse_args()
    if args.host and args.port:
        if not args.err:
            args.err = 0
        StartProgram(args.host,args.port,args.err)
    else:
        print('Type -h for help')

main()
