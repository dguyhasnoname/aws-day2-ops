import getopt, sys

class GetOpts:
    def get_opts():
        help, cluster, profile, output, sort, filter, namespace, verbose ='', '', '', '', '', '', '', ''
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc:p:o:s:f:v", ["help", "cluster=", "profile=", "output=", "sort=", "filter=", "verbose="])
        except getopt.GetoptError as err:
            print("[ERROR] {}. ".format(err) + \
            "Please run script with -h flag to see valid options.")
            sys.exit(0)

        for o, a in opts:
            if o in ("-h", "--help"):
                help = True
            elif o in ("-c", "--cluster"):
                cluster = a
            elif o in ("-p", "--profile"):
                profile = a                            
            elif o in ("-o", "--output"):
                output = a 
            elif o in ("-s", "--sort"):
                sort = a
            elif o in ("-f", "--filter"):
                filter = a
            elif o in ("-v", "--verbose"):
                verbose = True                                                                                       
 

        options = [help, cluster, profile, output, sort, filter, verbose]
        return options 