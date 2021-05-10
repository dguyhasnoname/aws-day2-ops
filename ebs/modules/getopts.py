import getopt, sys

class GetOpts:
    def get_opts():
        help, cluster, time, output, account='', '', 0, '', ''
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc:t:o:a:", ["help", "cluster", "time", "output", "account"])
        except getopt.GetoptError as err:
            print("[ERROR] {}. ".format(err) + \
            "Please run script with -h flag to see valid options.")
            sys.exit(0)

        for o, a in opts:
            if o in ("-h", "--help"):
                help = True
            elif o in ("-c", "--cluster"):
                cluster = a
            elif o in ("-t", "--time"):
                time = int(a)                
            elif o in ("-o", "--output"):
                output = a
            elif o in ("-a", "--account"):
                account = a                                         
            else:
                assert False, "unhandled option" 

        options = [help, cluster, time, output, account]
        return options 